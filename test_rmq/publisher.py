import pika
import jwt
import datetime
import os


def generate_jwt():
    key = "secret_key"
    payload = {
        'sub': '1234567890',
        'name': 'Denis',
        'admin': True,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, key)
    return token


def publish_message():
    rmq_user = os.getenv('RABBITMQ_USER')
    rmq_pass = os.getenv('RABBITMQ_PASSWORD')
    rmq_host = os.getenv('RABBITMQ_HOST')

    credentials = pika.PlainCredentials(rmq_user, rmq_pass)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rmq_host,
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)

    token = generate_jwt()
    message = f'Hellow World with JWT: {token}'

    channel.basic_publish(
        exchange='', 
        routing_key='hello',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f' [x] Sent {message}')

    connection.close()

publish_message()
