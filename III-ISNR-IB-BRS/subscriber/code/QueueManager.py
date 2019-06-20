import ssl
import pika

class QueueManager(object):
    """
    Queue Manager for RabbitMQ
    """
    def __init__(self, user, password, host, port, vhost, ssl=False):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.vhost = vhost
        self.ssl = ssl
        self.connect()

    """
    Connect to RabbitMQ
    """
    def connect(self):
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

    """
    Publish Message
    """
    def publish(self, exchange, routing_key, body):
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body, 
                                properties=pika.BasicProperties(delivery_mode = 2))

    """
    Declare Queue then binding
    """
    def declare_queue_binding(self, exchange, queue, key):
        self.channel.queue_declare(queue=queue,durable=True)
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key =key)
        
    """
    Close Connection
    """
    def disconnect(self):
        self.connection.close()

class QueueManagerUri(QueueManager):

    def __init__(self, uri):
        self.uri = uri
        self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.connection.URLParameters(self.uri))
        self.channel = self.connection.channel()
