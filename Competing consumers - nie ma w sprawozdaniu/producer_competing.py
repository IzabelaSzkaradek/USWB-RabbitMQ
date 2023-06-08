# consumers competing - consumer 2

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

# Bind the main queue to the main exchange
channel.queue_bind(exchange=main_exchange, queue=main_queue)

# Publish messages
message_count = 1000000
for i in range(1, message_count + 1):
    message = f'Message {i}'

    if i % 2 == 0 or i % 3 == 0:
        routing_key = 'consumer1'
    else:
        routing_key = 'consumer2'

    channel.basic_publish(
        exchange=main_exchange,
        routing_key=routing_key,
        body=message.encode(),  # Encode the message as bytes
        properties=pika.BasicProperties(delivery_mode=2)  # Make messages persistent
    )
    print(f'Published: {message} with routing key: {routing_key}')


# Close the connection
connection.close()
