from confluent_kafka import Consumer
import json
import time

consumer = Consumer({
    'bootstrap.servers': '192.168.127.38:9092',
    'group.id': 'test_group',
    'auto.offset.reset': 'smallest'
})
consumer.subscribe(['test'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    print('Received message: {}'.format(json.loads(msg.value())))
    time.sleep(1)
consumer.close()
