import pika

# Importowanie modułu pika, który jest biblioteką klienta do obsługi RabbitMQ.

# Nawiązywanie połączenia z RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Deklarowanie głównej wymiany (exchange) i kolejki (queue)
main_exchange = 'main_exchange'
main_queue = 'main_queue'

# Deklarowanie głównej wymiany
channel.exchange_declare(exchange=main_exchange, exchange_type='direct')

# Deklarowanie głównej kolejki z opcjami
queue_arguments = {
    'x-message-ttl': 10000,  # Ustawienie czasu życia wiadomości (w milisekundach)
    'x-dead-letter-exchange': 'dead_letter_exchange',  # Ustawienie wymiany dla martwych wiadomości
    'x-max-length': 100,  # Ustawienie maksymalnej długości kolejki
    'x-max-priority': 10  # Ustawienie maksymalnego priorytetu wiadomości
}
channel.queue_declare(queue=main_queue, durable=True, arguments=queue_arguments)

# Powiązanie głównej kolejki z główną wymianą
channel.queue_bind(exchange=main_exchange, queue=main_queue)

# Publikowanie wiadomości
message_count = 1000000
for i in range(1, message_count + 1):
    message = f'Wiadomość {i}'

    if i % 2 == 0 or i % 3 == 0:
        routing_key = 'consumer1'
    else:
        routing_key = 'consumer2'

    channel.basic_publish(
        exchange=main_exchange,
        routing_key=routing_key,
        body=message.encode(),  # Kodowanie wiadomości jako bajty
        properties=pika.BasicProperties(delivery_mode=2)  # Ustawienie trwałości wiadomości
    )
    print(f'Opublikowano: {message} z kluczem routingu: {routing_key}')

# Zamknięcie połączenia
connection.close()
