#-*- coding: utf-8-*-
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=  connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for servity in severities:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=servity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(' [x] %r:%r' % (method.routing_key, body))

channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()

# 多终端运行
# python routing_receive_logs.py info warning error
# python routing_receive_logs.py error
# python routing_emit_log.py error "run error balabala..."
# python routing_emit_log.py info "run info balabala..."
