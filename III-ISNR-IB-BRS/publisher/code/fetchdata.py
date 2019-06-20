import time, os, json, sys
from QueueManager import QueueManager
from IBMMQClient import IBMMQClientManager
import datetime


def DebugLog(msg,connectmsg):  
    """
    DebugLog
    開啟除錯模式(DebugLog=Open)時, 在程式執行目錄中的DebugLog資料夾，可查看執行過程的記錄檔。

    Args:
        msg:包含BPM及連線狀態的所有資訊，格式:BPM_西元年-月-日.txt
        connectmsg:僅有連線狀態的資訊，格式:Connect_西元年-月-日.txt

    """ 
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
            msg = connectmsg = str(datetime.datetime.now())+ " Connect success !! connectcount:" + str(connectcount) 
            DebugLog(msg,connectmsg)   
        except  Exception as pymqierror :
            keep_connect = True
            msg = connectmsg =str(datetime.datetime.now())+ " Connect fail !! connectcount:" + str(connectcount) + str(pymqierror) 
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
                    #How to get the message off a queue
                    msg_body = ibmmqi.getmessage()
                    msg = str(datetime.datetime.now())+ " success!! "+ msg_body       
                    getmessagecount  = getmessagecount + 1       
                    connectmsg = str(datetime.datetime.now())+ " success!! getmessagecount:" +str(getmessagecount)  
                    try:
                        if (qm.is_connected()) == False :
                            qm.connect()
                        qm.publish(exchange, routing_key, msg_body) 
                    except Exception as RabbitMQerror:
                        qm.connect()     
                        msg = connectmsg =str(datetime.datetime.now())+ ":" +str(count) + "RabbitMQerror Exception !! " +str(RabbitMQerror)                     
                    keep_running = True
                    keep_connect = False
                    count = 1                 
                except  Exception as pymqierror :  
                    exceptioncount  = exceptioncount + 1      
                    connectmsg =str(datetime.datetime.now())+ ":" +str(count) + " Exception !! exceptioncount:" +str(exceptioncount)+ "-" +str(pymqierror)
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
                    msg = connectmsg = str(datetime.datetime.now())+ " ibmmqi.close()!! "    
                    ibmmqi.close()
                except  Exception as pymqicloseerr :   
                    msg = connectmsg = str(datetime.datetime.now())+ " ibmmqi.close():Exception !! " +str(pymqicloseerr)
                DebugLog(msg,connectmsg)   
                time.sleep(1)             
    
        keep_connect = True
        try:
            ibmmqi.disconnect()  
            msg = connectmsg = str(datetime.datetime.now())+ " ibmmqi.disconnect! getmessagecount:" +str(getmessagecount)  
        except  Exception as pymqidisconerr :   
            msg = connectmsg = str(datetime.datetime.now())+ " ibmmqi.disconnect:Exception !! " +str(pymqidisconerr)
        DebugLog(msg,connectmsg)   
        time.sleep(DisconnectSec)    
        

if __name__ == "__main__":   
    mainfunction()
