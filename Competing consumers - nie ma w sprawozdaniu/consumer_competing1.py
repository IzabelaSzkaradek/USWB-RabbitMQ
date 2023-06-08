# consumers competing - consumer 1

import pika

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the main exchange and queue
main_exchange = 'main_exchange'
main_queue = 'main_queue'

# Declare the main exchange
channel.exchange_declare(exchange=main_exchange, exchange_type='direct')

# Declare the main queue with options
queue_arguments = {
    'x-message-ttl': 10000,  # Set message TTL (milliseconds)
    'x-dead-letter-exchange': 'dead_letter_exchange',  # Set dead letter exchange
    'x-max-length': 100,  # Set maximum queue length
    'x-max-priority': 10  # Set maximum message priority
}
channel.queue_declare(queue=main_queue, durable=True, arguments=queue_arguments)

# Bind the main queue to the main exchange with the routing key "consumer1"
channel.queue_bind(exchange=main_exchange, queue=main_queue, routing_key='consumer1')

# Set up a consumer callback function
def consumer_callback(ch, method, properties, body):
    message = body.decode()
    routing_key = method.routing_key
    print(f"Received message: {message} with routing key: {routing_key}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages
channel.basic_consume(queue=main_queue, on_message_callback=consumer_callback)

print('Consumer 1 started. Waiting for messages...')
channel.start_consuming()
