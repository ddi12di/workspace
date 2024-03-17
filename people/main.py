import asyncio
import functools
import json
import logging
from typing import Dict, Any
import pika
from fastapi import FastAPI, Depends, HTTPException
from pika.adapters.asyncio_connection import AsyncioConnection
from pika.exchange_type import ExchangeType
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

from requestapi.endpointcallback import get_data
from view.endpoint import view_data

app = FastAPI()

app.include_router(get_data)
app.include_router(view_data)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return Settings()

@app.post("/login")
def login(username: str, password: str, Authorize: AuthJWT = Depends()):
    if username == "admin" and password == "password":
        access_token = Authorize.create_access_token(subject=username)
        return {"access_token": access_token}
    raise HTTPException(status_code=401, detail="Unvalid username or password")


def on_connection_open_error(_unused_connection, err):
	logger.error('Connection open failed: %s', err)


class AsyncioRabbitMQ(object):
	EXCHANGE = 'message'
	EXCHANGE_TYPE = ExchangeType.topic
	PUBLISH_INTERVAL = 1
	QUEUE = 'text'
	ROUTING_KEY = 'example.text'

	def __init__(self, amqp_url):
		self._connection = None
		self._channel = None

		self._deliveries = []
		self._acked = 0
		self._nacked = 0
		self._message_number = 0

		self._stopping = False
		self._url = amqp_url

	def connect(self):
		logger.info('Connecting to %s', self._url)
		return AsyncioConnection(
			pika.URLParameters(self._url),
			on_open_callback=self.on_connection_open,
			on_open_error_callback=on_connection_open_error,
			on_close_callback=self.on_connection_closed)

	def on_connection_open(self, connection):
		logger.info('Connection opened')
		self._connection = connection
		logger.info('Creating a new channel')
		self._connection.channel(on_open_callback=self.on_channel_open)

	def on_connection_closed(self, _unused_connection, reason):
		logger.warning('Connection closed: %s', reason)
		self._channel = None

	def on_channel_open(self, channel):
		logger.info('Channel opened')
		self._channel = channel
		self.add_on_channel_close_callback()
		self.setup_exchange(self.EXCHANGE)

	def add_on_channel_close_callback(self):
		logger.info('Adding channel close callback')
		self._channel.add_on_close_callback(self.on_channel_closed)

	def on_channel_closed(self, channel, reason):
		logger.warning('Channel %i was closed: %s', channel, reason)
		self._channel = None
		if not self._stopping:
			self._connection.close()

	def setup_exchange(self, exchange_name):
		logger.info('Declaring exchange %s', exchange_name)
		# Note: using functools.partial is not required, it is demonstrating
		# how arbitrary data can be passed to the callback when it is called
		cb = functools.partial(self.on_exchange_declareok, userdata=exchange_name)
		self._channel.exchange_declare(exchange=exchange_name, exchange_type=self.EXCHANGE_TYPE, callback=cb)

	def on_exchange_declareok(self, _unused_frame, userdata):
		logger.info('Exchange declared: %s', userdata)
		self.setup_queue(self.QUEUE)

	def setup_queue(self, queue_name):
		logger.info('Declaring queue %s', queue_name)
		self._channel.queue_declare(queue=queue_name, callback=self.on_queue_declareok)

	def on_queue_declareok(self, _unused_frame):
		logger.info('Binding %s to %s with %s', self.EXCHANGE, self.QUEUE, self.ROUTING_KEY)
		self._channel.queue_bind(self.QUEUE, self.EXCHANGE, routing_key=self.ROUTING_KEY, callback=self.on_bindok)

	def on_bindok(self, _unused_frame):
		logger.info('Queue bound')
		self.start_publishing()

	def start_publishing(self):
		logger.info('Issuing Confirm.Select RPC command')
		self._channel.confirm_delivery(self.on_delivery_confirmation)

	def on_delivery_confirmation(self, method_frame):
		confirmation_type = method_frame.method.NAME.split('.')[1].lower()
		logger.info('Received %s for delivery tag: %i', confirmation_type, method_frame.method.delivery_tag)
		if confirmation_type == 'ack':
			self._acked += 1
		elif confirmation_type == 'nack':
			self._nacked += 1
		self._deliveries.remove(method_frame.method.delivery_tag)
		logger.info(
			'Published %i messages, %i have yet to be confirmed, '
			'%i were acked and %i were nacked', self._message_number,
			len(self._deliveries), self._acked, self._nacked)

	def publish_message(self, message):
		if self._channel is None or not self._channel.is_open:
			return

		hdrs = {"a": "b"}
		properties = pika.BasicProperties(
			app_id='example-publisher',
			content_type='application/json',
			headers=hdrs)

		self._channel.basic_publish(self.EXCHANGE, self.ROUTING_KEY,
		                            json.dumps(message, ensure_ascii=False),
		                            properties)
		self._message_number += 1
		self._deliveries.append(self._message_number)
		logger.info('Published message # %i', self._message_number)


ep = None


# @app.on_event("startup")
# async def startup() -> None:
# 	global ep
# 	await asyncio.sleep(10)
# 	user = "guest"
# 	passwd = "guest"
# 	host = "127.0.0.1"
# 	port = "5672"

# 	ep = AsyncioRabbitMQ(f'amqp://{user}:{passwd}@{host}:{port}/%2F')
# 	ep.connect()


JSONObject = Dict[str, Any]


@app.post("/webhook")
async def webhook_endpoint(msg: JSONObject, Authorize: AuthJWT = Depends()):
	Authorize.jwt_required()
	global ep
	ep.publish_message(msg)
	return 204


async def process_order(ch, method, properties, body):
	# Здесь происходит обработка заказа
	print("Получен заказ:", body)
	# Подтверждение обработки заказа
	ch.basic_ack(delivery_tag=method.delivery_tag)

async def consume_orders(channel):
	await channel.basic_consume(queue='orders', on_message_callback=process_order)

async def setup_rmq():
	connection = await AsyncioConnection(pika.ConnectionParameters('rabbitmq'))
	channel = await connection.channel()
	await channel.queue_declare('orders')
	asyncio.create_task(consume_orders(channel))

	# connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
	# channel = connection.channel()
	# channel.queue_declare('orders')
	# channel.basic_consume('orders', on_message_callback=process_order)
	# channel.start_consuming()

async def main():
	await setup_rmq()
	await asyncio.create_task(app.run())

if __name__ == "__main__":
	asyncio.run(main())