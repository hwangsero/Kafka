import json
import requests
from confluent_kafka import Producer
import time

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
  
producer = Producer({'bootstrap.servers': '192.168.127.38:9092'})
while True:
    api_server='http://127.0.0.1:5001/api'
    request=requests.get(api_server)
    data=json.loads(request.content)
    json_data = json.dumps(data)
    producer.poll(0)
    producer.produce("test", json_data, callback=delivery_report)
    producer.flush()
    time.sleep(1)
