# -*- coding: utf-8 -*-
import time, os, json, sys
import datetime
from QueueManager import QueueManager
from IBMMQClient import IBMMQClientManager
from portalLog import PortalLog as plog

# #機場
# url = "http://172.20.0.228:5555/baggages/api/v1/bpm/"
# token = "0d7bb5e553351702b633ccfe46c93fa007f6e4f1"


# #會內
# url = "http://124.9.14.14:5555/baggages/api/v1/bpm/"
# token = "019d09a5b4dc82f96faa2c010d8dee40f794e033"

def DebugLog(msg, connectmsg, eventLog, count):  
    """
    DebugLog
    開啟除錯模式(DebugLog=Open)時, 在程式執行目錄中的DebugLog資料夾，可查看執行過程的記錄檔。

    Args:
        msg:包含BPM及連線狀態的所有資訊，格式:BPM_西元年-月-日.txt

        connectmsg:僅有連線狀態的資訊，格式:Connect_西元年-月-日.txt

        ceventLog:稽查資料，透過API傳送至Web Server。

        count:紀錄此稽查資料是否為BPM資訊。1:取得BPM資訊; 0:非BPM資訊的其他系統稽查資訊。   
             
    """ 
    DebugLogDir = os.path.dirname(__file__) #<-- absolute dir the script is in   
    DebugLogDir = os.path.join(DebugLogDir, '..')   
    DebugLogDir = os.path.join(DebugLogDir, 'DebugLog')
    DebugLog = os.getenv('DebugLog')
    
    
    if eventLog :                
        plog.sentLog(str(eventLog),count)

    if connectmsg :                
        connectmsg = str(datetime.datetime.now())+ " " + connectmsg     
    if msg :  
        msg = str(datetime.datetime.now())+ "@" + msg + "@"  


    if DebugLog.upper() == "OPEN" :
        if not os.path.exists('DebugLog'):
            try:
                os.makedirs('DebugLog')
            except Exception as patherror :
                print(str(patherror))        
        if msg : 
            with open(os.path.join(DebugLogDir, "BPM_"+str(datetime.datetime.now().date())+".txt") , "a") as text_file:
                print(f"{msg}", file=text_file)                
        if connectmsg :          
            with open(os.path.join(DebugLogDir, "Connect_"+str(datetime.datetime.now().date())+".txt") , "a") as text_file:
                print(f"{connectmsg}", file=text_file)   
    else:
        if msg :            
            print(str(msg)) 
    if connectmsg :        
        print(str(connectmsg))



def mainfunction(): 
    """
    mainfunction
    分別與IBM MQ及Rabbit MQ建立連線通道，進行從IBM MQ Server取得BPM資料，將取得的原始內文，直接publish傳送到Rabbit MQ 的BPM序列中。
    除此之外，導入連線例外狀況的容錯處理，重複使用已建立的連線通道，降低建立連線通道成本。
    主系統程式架構，由兩大迴圈組成，外層迴圈管控與Server的連線，內層迴圈管控BPM資料取得及傳送。利用FailToSleepSec及DisconnectSec參數，設定連線處理的等待時間。
    
    FailToSleepSec: 設定程式例外處理的休眠時間，包括”NO_MSG”的處理。
    
    DisconnectSec: 設定程式與IBM MQ Server離線後，重新連線的隔間等待時間。

    """
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
    exceptioncount = 0
    getmessagecount = 0
    connectcount = 0
    while keep_connect:
        try:
            ibmmqi.connect(user, password)                 
            keep_connect = False 
            connectcount = connectcount + 1    
            msg = connectmsg = "Connect success !! connectcount:" + str(connectcount) 
            DebugLog(msg,connectmsg,'MqConnectSucces','0')   
        except  Exception as pymqierror :
            keep_connect = True
            msg = connectmsg ="Connect fail !! connectcount:" + str(connectcount) + str(pymqierror) 
            DebugLog(msg,connectmsg,'MqConnectFail','0') 
        time.sleep(1)
        if keep_connect == False : 
            #Connecting in client mode
            ibmmqi.Queue()
            keep_running = True
            count = 1
            
            while keep_running:                
                msg = connectmsg =" keep_running is true!! " 
                try:                       
                    #How to get the message off a queue
                    msg_body = ibmmqi.getmessage()
                    msg = "Success!! "+ msg_body       
                    getmessagecount  = getmessagecount + 1       
                    connectmsg = "IBMMQ  getmessage success!! getmessagecount:" +str(getmessagecount)  
                    DebugLog(msg,connectmsg,'GetMesFormIbmMQ','1')    
                    try:
                        if (qm.is_connected()) == False :
                            qm.connect()
                        qm.publish(exchange, routing_key, msg_body)    
                        connectmsg = "RabbitMQ publisher success!! getmessagecount:" +str(getmessagecount)  
                        DebugLog(msg,connectmsg,'BpmToRabbbitMQ','0')      
                    except Exception as RabbitMQerror:
                        qm.connect()     
                        msg = connectmsg = ":" +str(count) + "RabbitMQerror Exception !! " +str(RabbitMQerror)                     
                        DebugLog(msg,connectmsg,'RabbitMqError','0')  
                    keep_running = True
                    keep_connect = False
                    count = 1                 
                except  Exception as pymqierror :  
                    exceptioncount  = exceptioncount + 1      
                    connectmsg = ":" +str(count) + " Exception !! exceptioncount:" +str(exceptioncount)+ "-" +str(pymqierror)
                    if count > 9 :
                        keep_running = False            
                        keep_connect = True
                    else:
                        keep_running = True
                        keep_connect = False
                    count = count + 1    
                    DebugLog(msg,connectmsg,'IbmMQException','0')        
                    time.sleep(FailToSleepSec)       
                #time.sleep(2)
            
            if keep_running == False:         
                keep_connect = True
                try:                    
                    msg = connectmsg = "ibmmqi.close()!! "    
                    ibmmqi.close()
                except  Exception as pymqicloseerr :   
                    msg = connectmsg ="ibmmqi.close():Exception !! " +str(pymqicloseerr)
                DebugLog(msg,connectmsg,'IbmMqClose','0')    
                time.sleep(1)             
    
        keep_connect = True
        try:
            ibmmqi.disconnect()  
            msg = connectmsg = "ibmmqi.disconnect! getmessagecount:" +str(getmessagecount)  
        except  Exception as pymqidisconerr :   
            msg = connectmsg = "ibmmqi.disconnect:Exception !! " +str(pymqidisconerr)        
        DebugLog(msg,connectmsg,'IbmMqDisconnect','0')    
        time.sleep(DisconnectSec)    
        

if __name__ == "__main__":   
    mainfunction()
