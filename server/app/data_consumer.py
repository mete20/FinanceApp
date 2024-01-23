import pika
import pandas as pd
import sqlite3

def update_stock_table(symbol, price):
    conn = sqlite3.connect('my_database.db') # actual database name
    cursor = conn.cursor()
    cursor.execute("UPDATE stock_table SET price = ? WHERE symbol = ?", (price, symbol)) # stock_table should be the table name
    conn.commit()
    conn.close()

def consume_stock_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='stock_data')

    def callback(ch, method, properties, body):
        symbol, price = body.decode().split(':')
        update_stock_table(symbol, price)

    channel.basic_consume(queue='stock_data', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
