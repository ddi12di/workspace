import pika
import jwt
import os

import sys
sys.stdout = sys.stderr


def callback(ch, method, properties, body):
    try:
        decoded_token = jwt.decode(body, "secret_key", ["HS256"])
        print(f" [x] Recieved {decoded_token['message']}")
    except jwt.InvalidTokenError as e:
        print(str(e))


def start_consumer():
    rmq_user = os.getenv('RABBITMQ_USER')
    rmq_pass = os.getenv('RABBITMQ_PASSWORD')
    rmq_host = os.getenv('RABBITMQ_HOST') 

    print(rmq_user, rmq_pass, rmq_host)

    credentials = pika.PlainCredentials(rmq_user, rmq_pass)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rmq_host,
            credentials=credentials,
            connection_attempts=10,
            retry_delay=5,
            socket_timeout=10
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hello', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

start_consumer()
