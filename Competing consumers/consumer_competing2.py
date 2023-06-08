# consumers competing - producer

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

# Powiązanie głównej kolejki z główną wymianą za pomocą klucza routingu "consumer2"
channel.queue_bind(exchange=main_exchange, queue=main_queue, routing_key='consumer2')

# Ustawienie funkcji zwrotnej (callback) dla konsumenta
def consumer_callback(ch, method, properties, body):
    message = body.decode()
    routing_key = method.routing_key
    print(f"Otrzymano wiadomość: {message} z kluczem routingu: {routing_key}")

    # Potwierdzenie odbioru wiadomości
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Rozpoczęcie odbierania wiadomości
channel.basic_consume(queue=main_queue, on_message_callback=consumer_callback)

print('Konsument 2 rozpoczął działanie. Oczekiwanie na wiadomości...')
channel.start_consuming()
