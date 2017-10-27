# -*- coding: utf-8 -*-
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or 'Hello World!'
channel.basic_publish(exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2
    ))
print(" [x] Sent %r " % message)
connection.close()

# 多终端运行
# python work_queue_worker.py
# python work_queue_worker.py
# python work_queue_new_tasks.py
