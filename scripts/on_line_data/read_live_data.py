#!/bin/python
from kafka import KafkaConsumer
import sys

topic = sys.argv[1]
group = 'live_zipline_reader'
servers = ['cscs-28-163-1-64.fzzqxf.com:9092', 'cscs-28-163-1-63.fzzqxf.com:9092', 'cscs-28-163-1-62.fzzqxf.com:9092',
           'cscs-28-163-1-61.fzzqxf.com:9092']

consumer = KafkaConsumer(topic,
                         group_id=group,
                         bootstrap_servers=servers)
try:
    for message in consumer:
        print(str(message.value, 'utf-8'))

except KeyboardInterrupt:
    print("Catch Keyboard interrupt")
