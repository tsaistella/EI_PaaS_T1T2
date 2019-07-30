# -*- coding: utf-8 -*-
import ssl
import pika

class QueueManager(object):    
    def __init__(self, user, password, host, port, vhost, ssl=False):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.vhost = vhost
        self.ssl = ssl
        self.connect()


    def connect(self):
        """
        connect        
		與RabbitMQ Server建立連線。
        """
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        ssl_options = pika.SSLOptions(context) if self.ssl else None
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.host, \
                                                self.port, \
                                                self.vhost, \
                                                credentials, ssl_options=ssl_options)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def is_connected(self):
        """
        is_connected
		判斷與RabbitMQ Server的連線狀況。
        """  
        return self.connection.is_open


    def publish(self, exchange, routing_key, body):
        """
        publish
        傳送資訊到佇列中
        """
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body, 
                                properties=pika.BasicProperties(delivery_mode = 2))

    
    def declare_queue_binding(self, exchange, queue, key):
        """
        declare_queue_binding
        宣告挷定佇列
        """
        self.channel.queue_declare(queue=queue,durable=True)
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key =key)
        
    def disconnect(self):        
        """        
        disconnect        
		切斷與RabbitMQ Server的連線。
        """
        self.connection.close()
