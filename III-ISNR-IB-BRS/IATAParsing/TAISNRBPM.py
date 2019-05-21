import pymqi 

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
queue = pymqi.Queue(qmgr, queue_name)


#How to put the message on a queue
# try:
#     queue.put(message)
# except Exception as identifier:
#     print(str(identifier))


keep_running = True
while keep_running:
    try:


        #How to get the message off a queue
        stella = queue.get()

        print(stella.decode('utf-16'))
        
    except  Exception as pymqierror :
        print(str(pymqierror))


queue.close()

qmgr.disconnect()