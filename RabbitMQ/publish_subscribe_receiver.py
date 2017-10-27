#-*- coding: utf-8-*-
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel= connection.channel()

# 声明一个exchange（exchange名为logs，类型为fanout）
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# 当consumer断开连接时，自动删除队列。
result = channel.queue_declare(exclusive=True)
# 为队列创建一个随机的队列名，e.g. amq.gen-JzTY20BRgKO-HjmUJj0wLg
queue_name = result.method.queue
# 把exchange和queue关联（bindings）起来
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

# 回调函数
def callback(ch, method, properties, body):
    print(" [x] %r" % body)

# 为queue指定回调函数
channel.basic_consume(callback, queue=queue_name, no_ack=True)
# 开始消费
channel.start_consuming()
