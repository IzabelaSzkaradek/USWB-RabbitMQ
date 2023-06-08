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

# Usunięcie istniejącej kolejki głównej, jeśli już istnieje
channel.queue_delete(queue=main_queue)

# Deklaracja głównej kolejki z opcjami
queue_arguments = {
    'x-message-ttl': 10000,  # Ustawienie czasu życia wiadomości (w milisekundach)
    'x-dead-letter-exchange': 'dead_letter_exchange',  # Ustawienie wymiany kolejki martwej
    'x-max-length': 100,  # Ustawienie maksymalnej długości kolejki
    'x-max-priority': 10  # Ustawienie maksymalnego priorytetu wiadomości
}
channel.queue_declare(queue=main_queue, durable=True, arguments=queue_arguments)

# Definicja funkcji zwrotnej dla konsumowania wiadomości
def callback(ch, method, _, body):
    print(f'Otrzymano: {body}')
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Potwierdzenie odebrania wiadomości

# Konsumowanie wiadomości
channel.basic_consume(queue=main_queue, on_message_callback=callback)

# Rozpoczęcie konsumowania w osobnym wątku
channel.start_consuming()


