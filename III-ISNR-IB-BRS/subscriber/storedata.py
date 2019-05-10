#!/usr/bin/env python
import os
import sys
import time
import pika
from QueueManager import QueueManager
from WebRequestManager import WebRequestManager as webmgr
from IATAParsing import IATAParsing  as IataParsing

# # RabbitMQ Variables
user = os.getenv('RABBITMQ_USER')
password = os.getenv('RABBITMQ_PASSWORD')
host = os.getenv('RABBITMQ_HOST')
port = os.getenv('RABBITMQ_PORT')
vhost = os.getenv('RABBITMQ_VHOST')
queue_name = os.getenv('RABBITMQ_QUEUENAME')

def parse_store( body):
    #print(body)
	#txt = "BPM\r\n.V/1LTPE\r\n.J/R///18APR/002903L/TIAT2/\r\n.F/BR0026/17APR/SEA/Y\r\n.B/UNS/0695463055001\r\n.I/BR0266/17APR/PNH/Y\r\n.S/Y/70D/C/080/080//Y/A\r\n.W/K/1/17\r\n.P/ROS/SARAMONICH\r\nENDBPM"
    json_str = IataParsing.IATABPM(body)    
    print ("JSON：", json_str)
    url = ""
    #webmgr.post_json(url, json_str, True, False, None)
    

def dataParsing():  
    #user = "isnr"
    #password = "isnr2019"
    #host = "172.20.0.220"
    #port = 5671
    #vhost = "isnr"
    #queue_name = "bpm"


    qm = QueueManager(user, password, host, port, vhost, True)
    channel = qm.channel

    
    def callback(ch, method, properties, body):
        parse_store(body)
    channel.basic_consume(queue_name, callback ,auto_ack=True)
    print(' [*] Waiting for messages.')
    try:
        channel.start_consuming()
    except pika.exceptions.ChannelClosedByBroker as e:
        sys.exit('Error: cannot connect to RqbbitMQ!')

if __name__ == "__main__":
    dataParsing()
