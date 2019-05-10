import time, os, json, sys
from QueueManager import QueueManager, QueueManagerUri
import pymqi 

#stella from WebRequestManager import WebRequestManager as webmgr

from init import init_queue
from config import FOS_API

def fetchdata():
    
    # === Local ===
    # # RabbitMQ Variables
    # user = os.getenv('RABBITMQ_USER')
    # password = os.getenv('RABBITMQ_PASSWORD')
    # host = os.getenv('RABBITMQ_HOST')
    # port = os.getenv('RABBITMQ_PORT')
    # vhost = os.getenv('RABBITMQ_VHOST')
    
    # exchange = os.getenv('RABBITMQ_EXCHANGE')
    user = "isnr"
    password = "isnr2019"
    host = "172.20.0.220"
    port = 5671
    vhost = "isnr"

    qm = QueueManager(user, password, host, port, vhost, True)
    # TODO: Add feature for switch local and cloud app setting

    # === Cloud App ===
    # # Load RabbitMQ from system variable
    # vcap_services_json = os.getenv('VCAP_SERVICES')
    # vcap_services = json.loads(vcap_services_json)


    # # Cannot get RabbitMQ settings 
    # if 'p-rabbitmq' not in vcap_services and len(vcap_services['p-rabbitmq']) < 1:
    #     sys.exit('Error: cannot get RabbitMQ settings!')

    # rabbitmq_uri = vcap_services['p-rabbitmq'][0]['credentials']['protocols']['amqp']['uri']

    exchange ="bpm"

    # initial queues
    init_queue(qm, exchange)
    
    # TODO: Split main function for oop

    queue_manager = "TIABPM"
    channel = "TAISNR.SVRCONN"
    host = "10.2.67.76"
    port = "1414"
    queue_name = "TAISNR.LOCAL.QUEUE"
    message = 'Hello from Python!'
    conn_info = "%s(%s)" % (host, port)

    pymqi.queue_manager = queue_manager
    pymqi.channel = channel
    pymqi.host = host
    pymqi.port = port
    pymqi.queue_name = queue_name
    pymqi.conn_info = conn_info

    #qmgr = pymqi.connect(queue_manager, channel, conn_info)
    #Connecting in client mode with username/password credentials
    user = 'TAISNRBPM'
    password = 'Taisnr123456!'
    qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)


    #Connecting in client mode
    ibmqueue = pymqi.Queue(qmgr, queue_name)
            
        #How to put the message on a queue
    # try:
    #     ibmqueue.put(message)
    # except Exception as identifier:
    #     print(str(identifier))

    keep_running = True
    while keep_running:
        try:
            #How to get the message off a queue
            msg_body = ibmqueue.get().decode('utf-16')
            print(msg_body)            
            # routing_key = '{}_rk'.format(api['name'].lower())            
            routing_key = "bpm_rk"
            qm.publish(exchange, routing_key, msg_body)
        except  Exception as pymqierror :
            print(str(pymqierror))

    ibmqueue.close()

    qmgr.disconnect()

if __name__ == "__main__":
    fetchdata()
