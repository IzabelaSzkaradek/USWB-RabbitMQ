# alternative exchange & dead letter exchange
import pika

# Nawiązanie połączenia z RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Deklaracja głównej wymiany i kolejki
main_exchange = 'main_exchange'
main_queue = 'main_queue'

# Deklaracja głównej wymiany
channel.exchange_declare(exchange=main_exchange, exchange_type='direct')

# Deklaracja głównej kolejki z opcjami
queue_arguments = {
    'x-message-ttl': 10000,  # Ustawienie czasu życia wiadomości (w milisekundach)
    'x-dead-letter-exchange': 'dead_letter_exchange',  # Ustawienie wymiany kolejki martwej
    'x-max-length': 100,  # Ustawienie maksymalnej długości kolejki
    'x-max-priority': 10  # Ustawienie maksymalnego priorytetu wiadomości
}
channel.queue_declare(queue=main_queue, durable=True, arguments=queue_arguments)

# Połączenie kolejki głównej z główną wymianą
channel.queue_bind(exchange=main_exchange, queue=main_queue)

# Publikowanie wiadomości
message_count = 10
for _ in range(message_count):
    for i in range(1, message_count+1):
        message = f'Wiadomość {i}'
        channel.basic_publish(
            exchange=main_exchange,
            routing_key='',
            body=message.encode(),  # Zakodowanie wiadomości jako bajty
            properties=pika.BasicProperties(delivery_mode=2)  # Ustawienie trwałości wiadomości
        )
        print(f'Opublikowano: {message}')

    # Zwiększenie liczby wiadomości dla kolejnej iteracji
    message_count *= 10

# Zamknięcie połączenia
connection.close()
