import time, os, json, sys
from QueueManager import QueueManager
from IBMMQClient import IBMMQClientManager
import datetime


def DebugLog(msg,connectmsg):
    DebugLog = os.getenv('DebugLog')
    if DebugLog.upper() == "OPEN" :
        if not os.path.exists('DebugLog'):
            try:
                os.makedirs('DebugLog')
            except Exception as patherror :
                print(str(patherror))        
        if msg :  
            with open("DebugLog\BPM_"+str(datetime.datetime.now().date())+".txt", "a") as text_file:
                print(f"{msg}", file=text_file)                
        if connectmsg :          
            with open("DebugLog\Connect_"+str(datetime.datetime.now().date())+".txt", "a") as text_file:
                print(f"{connectmsg}", file=text_file)   
    else:
        if msg :            
            print(str(msg)) 
    if connectmsg :        
        print(str(connectmsg))



def mainfunction(): 
    # === Local ===
    
    FailToSleepSec = int(os.getenv('FailToSleepSec'))
    DisconnectSec = int(os.getenv('DisconnectSec'))

    # # RabbitMQ Variables
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASSWORD')
    host = os.getenv('RABBITMQ_HOST')
    port = os.getenv('RABBITMQ_PORT')
    vhost = os.getenv('RABBITMQ_VHOST')
    exchange = os.getenv('RABBITMQ_BPMEXCHANGE')        
    routing_key = os.getenv('RABBITMQ_ROUTING_KEY')
    queue = os.getenv('RABBITMQ_QUEUENAME')   
    #user = "isnr"
    #password = "isnr2019"
    #host = "172.20.0.220"
    #port = 5671
    #vhost = "isnr"
    #exchange ="bpm"
    #routing_key = 'bpm_rk'
    qm = QueueManager(user, password, host, port, vhost, True)    

    # initial queues
    qm.declare_queue_binding(exchange, queue, routing_key)

  
    # # IBMMQ Variables
    queue_manager = os.getenv('IBMQUEUE_MANAGER')    
    channel = os.getenv("IBMCHANNEL")
    host = os.getenv("IBMHOST")
    port = os.getenv("IBMPORT")
    queue_name = os.getenv("IBMQUEUE_NAME")
    user = os.getenv('IBMUSER')
    password = os.getenv('IBMPASSWORD')
    #queue_manager = "TIABPM"
    #channel = "TAISNR.SVRCONN"
    #host = "10.2.67.76"
    #port = "1414"
    #queue_name = "TAISNR.LOCAL.QUEUE"
    #user = 'TAISNRBPM'
    #password = 'Taisnr123456!'
    conn_info = "%s(%s)" % (host, port)
    ibmmqi = IBMMQClientManager(queue_manager, channel, host, port, queue_name, conn_info)
    

    keep_connect = True
    msg = ""
    connectmsg  = ""
    while keep_connect:
        try:               
            ibmmqi.connect(user, password)                 
            keep_connect = False   
            msg = connectmsg = str(datetime.datetime.now())+ " Connect success !! "    
            DebugLog(msg,connectmsg)   
        except  Exception as pymqierror :
            keep_connect = True
            msg = connectmsg =str(datetime.datetime.now())+ " Connect fail !! " +str(pymqierror) 
            DebugLog(msg,connectmsg) 
        time.sleep(1)
        if keep_connect == False : 
            #Connecting in client mode
            ibmmqi.Queue()
            keep_running = True
            count = 1
            
            while keep_running:                
                msg = connectmsg =" keep_running is true!! " 
                try: 
                    if ibmmqi.is_connected :                        
                        msg = connectmsg =" ibmmqi.is_connected is true!! " 
                        #How to get the message off a queue
                        msg_body = ibmmqi.getmessage()
                        msg = str(datetime.datetime.now())+ " success!! "+ msg_body
                        connectmsg = str(datetime.datetime.now())+ " success!! "          
                        try:
                            if qm.is_connected == False :
                                qm.connect()
                            qm.publish(exchange, routing_key, msg_body) 
                        except Exception as RabbitMQerror:
                            qm.connect()     
                            msg = connectmsg =str(datetime.datetime.now())+ ":" +str(count) + "RabbitMQerror Exception !! " +str(RabbitMQerror)                     
                        keep_running = True
                        keep_connect = False
                        count = 1 
                    else :   
                        keep_running = False            
                        keep_connect = True
                        msg = connectmsg = str(datetime.datetime.now())+ " sucibmmqi.is_connected: false, break while!! " 
                except  Exception as pymqierror :     
                    msg = connectmsg =str(datetime.datetime.now())+ ":" +str(count) + " Exception !! " +str(pymqierror)
                    if count > 9 :
                        keep_running = False            
                        keep_connect = True
                    else:
                        keep_running = True
                        keep_connect = False
                    count = count + 1         
                    time.sleep(FailToSleepSec)    
                DebugLog(msg,connectmsg)          
                #time.sleep(2)
            
            if keep_running == False:         
                keep_connect = True
                try:                    
                    msg = connectmsg = " ibmmqi.close()!! "    
                    ibmmqi.close()
                except  Exception as pymqicloseerr :   
                    msg = connectmsg = str(datetime.datetime.now())+ " ibmmqi.close():Exception !! " +str(pymqicloseerr)
                DebugLog(msg,connectmsg)   
                time.sleep(1)             
    
        keep_connect = True
        try:
            ibmmqi.disconnect()  
            msg = connectmsg = str(datetime.datetime.now())+ " ibmmqi.disconnect! "            
        except  Exception as pymqidisconerr :   
            msg = connectmsg = str(datetime.datetime.now())+ " ibmmqi.disconnect:Exception !! " +str(pymqidisconerr)
        DebugLog(msg,connectmsg)   
        time.sleep(DisconnectSec)    
        

if __name__ == "__main__":   
    mainfunction()
