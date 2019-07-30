# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys
import time
import pika
import datetime
from QueueManager import QueueManager
from WebRequestManager import WebRequestManager as webmgr
from IATAParsing import IATAParsing  as IataParsing
from portalLog import PortalLog as plog

# # RabbitMQ Variables
user = os.getenv('RABBITMQ_USER')
password = os.getenv('RABBITMQ_PASSWORD')
host = os.getenv('RABBITMQ_HOST')
port = os.getenv('RABBITMQ_PORT')
vhost = os.getenv('RABBITMQ_VHOST')
queue_name = os.getenv('RABBITMQ_QUEUENAME')
url = os.getenv('PORTAL_URL')
token = os.getenv('PORTAL_TOKEN')

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
        msg:包含BPM及連線狀態的所有資訊，格式:BPMJSON_西元年-月-日.txt

        connectmsg:僅有連線狀態的資訊，格式:Connect_西元年-月-日.txt

        eventLog:稽查資料，透過API傳送至Web Server。

        count:紀錄此稽查資料是否為BPM資訊。1:取得BPM資訊; 0:非BPM資訊的其他系統稽查資訊。   
             
    """ 

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in   
    script_dir = os.path.join(script_dir, '..')   
    script_dir = os.path.join(script_dir, 'DebugLog')
    sBPMJSON = "BPMJSON_"+str(datetime.datetime.now().date())+".txt"
    sConnect = "Connect_"+str(datetime.datetime.now().date())+".txt"

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
            with open(os.path.join(script_dir, sBPMJSON) , "a") as text_file:
                print(f"{msg}", file=text_file)                
        if connectmsg :     
            with open( os.path.join(script_dir, sConnect) , "a") as text_file:
                print(f"{connectmsg}", file=text_file)   
    else:
        if msg :            
            print(str(msg)) 
    if connectmsg :                   
        print(str(connectmsg))


def dataParsing(body): 
    """
    dataParsing
    將從Rabbit MQ Server取得原始BPM內文資料，進行格式語意的Parse，以JSON形式輸出呈現。
    """
    json_str = ''
    try:
        json_str = IataParsing.IATABPM(body)  
    except Exception as IATABpmError :
        raise IATABpmError
    else:    
        return json_str
    

def parseStore(json_str):
    """
    parseStore
    透過API 將資料傳送至Web Server，且導入連線例外狀況的容錯處理，連續10次傳送失敗，會將傳送內文輸出打印。
    """    
    webmgr_connect = True   
    count = 1
    while webmgr_connect:
        try:    
            result = webmgr.post_json(url, json_str, token=token)
            if result.status_code != 201:
                print(result.text)
                print(json_str)
            else:
                DebugLog('','Send BPM to PORTAL Success!','BPMtoPORTAL' ,'0') 
            webmgr_connect = False 
        except Exception as patherror :
            print(str(patherror))     
            if count > 9 :
                print ("JSON：", json_str)
                webmgr_connect = False  
            count = count + 1  

            
src_file_path = ''

def mainfunction(source):  
    """
    mainfunction
    主要功能:取得BPM資料，並且將Parse語意後的BPM JSON格式資料傳送至Web Server。目前系統支援 由(1)Rabbit MQ 或(2)LOG檔 ，兩種取得BPM來源。

    (1) 與Rabbit MQ建立連線通道，監聽等待從Rabbit MQ Server取得原始BPM內文資料，以callback方法啟動IataParsing，並且將Parse語意後的BPM JSON格式資料傳送至Web Server。
     除此之外，導入連線例外狀況的訊習提示且中斷服務，由CF 管理系統再自動啟動程式。
     
     SOURCE:'RabbitMQ'-來源是從RabbitMQ Server中取得未Parse語意過的BPM資訊，需要先進行Parse語意，再傳送至Web Server。
 
    (2) 取得SourceLog資料夾中的BPM 記錄文件檔，可運用於系統容錯處理，使用BPM文件記錄檔，補缺少(或需增加)的BPM資訊，再傳送Parse語意後的BPM JSON格式資料傳送至Web Server。
     
     SOURCE:'bpmOrg'-來源是從文件中取得未Parse語意過的BPM資訊，需要先進行Parse語意，再傳送至Web Server。
     
     SOURCE:'bpmJson'-來源是從文件中取得已Parse語意過的BPM資訊，只需要進行傳送至Web Server。
    """
    
    if 'RabbitMQ'.lower() in source.lower():
        # user = "isnr"
        # password = "isnr2019"
        # host = "172.20.0.220"
        # port = 5671
        # vhost = "isnr"
        # queue_name = "bpm"
        
        source = "source:" + source.lower().replace("mq",'MQ').replace("r",'R')
        DebugLog('',source,source,'0') 
        def callback(ch, method, properties, body):
            #print(type(body)) #<class 'dict'>
            data = str(body, 'utf-8')
            json_str = ''
            msg = data
            try:
                DebugLog('','Get message from RabbitMQ Server!!','GetBpmFomMQ','1') 
                json_str = dataParsing(data)
                msg =  str(json_str)                 
                parseStore(json_str)
            except Exception as error :
                DebugLog(msg,str(error),'GetBpmFomMQFAIL','0') 
        try:
            qm = QueueManager(user, password, host, port, vhost, True)
            channel = qm.channel   
            channel.basic_consume(queue_name, callback ,auto_ack=True)
            DebugLog('','Connected to RabbitMQ Server and Waiting for messages.','WaitBpmMsg','0') 
            print('Waiting for messages.') 
            channel.start_consuming()
        except Exception as e :
            DebugLog('','pika.exceptions: cannot connect to RabbitMQ! '+str(e.args),'Alert_MqFail' ,'0') 
            sys.exit('Error: cannot connect to RabbitMQ!')

    elif 'bpmOrg'.lower() in source.lower() or 'bpmJson'.lower() in source.lower():
        source = "source:" + source.lower() 
        DebugLog('',source,source,'0') 
        try:
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in   
            script_dir = os.path.join(script_dir, '..')   
            script_dir = os.path.join(script_dir, 'SourceLog')
            entries = os.listdir(script_dir)
        except Exception as e :
            DebugLog( '','FileNotFound: ' + str(e.args[1]) + ' - ' +  str(script_dir),'FileNotFound','0') 
            sys.exit('Error: FileNotFound!!')
        else:
            
            if not os.path.exists('DoneLog'):
                try:
                    os.makedirs('DoneLog')
                except Exception as patherror :
                    print(str(patherror))  
                    DebugLog( '',str(patherror),'MakedirFail','0') 
                    sys.exit('Error: Make DoneLog dir fail !!')
            for entry in entries:         
                try: 
                    bopenfile = False 
                    sfileBpmList = ''
                    src_file_path = os.path.join(script_dir, entry)  
                    dst_file_path = os.path.join(script_dir.replace('SourceLog','DoneLog'), 'Done'+entry) 
                    txt = ''
                    
                    DebugLog( '',src_file_path,entry,'0') 
                    with open(src_file_path, 'r') as f:
                        txt = f.read()     
                        bopenfile = True 
                        f.close()                        
                        if os.path.exists(dst_file_path):
                            #os.remove (dst_file_path)                            
                            os.rename (dst_file_path,  dst_file_path+str(datetime.datetime.now().date())) 
                        os.rename (src_file_path,  dst_file_path) 
                        if 'bpmOrg'.lower() in source.lower():                                 
                            txt = txt.replace(" BPM",'@BPM') 
                            txt = txt.replace("ENDBPM",'ENDBPM@')    
                        txt = txt.replace("\r",'')  
                        txt = txt.replace("\n",'\r\n')
                        txt = txt.replace("\r\n\r\n",'\r\n') 
                        sfileBpmList = txt.split("@", )  
                except Exception as patherror :
                    DebugLog( '',str(patherror),'Alert_pathError','0') 
                    raise patherror
                else:
                    if sfileBpmList != '' and bopenfile == True :
                        ifileBpmcount = 0
                        for ifileBpmList in range(len(sfileBpmList)):
                            if 'BPM' in sfileBpmList[ifileBpmList] : 
                                ifileBpmcount = ifileBpmcount + 1 
                                json_str = ''
                                data = sfileBpmList[ifileBpmList]   
                                try:
                                    msg = data
                                    if 'Rawdata' not in sfileBpmList[ifileBpmList] : 
                                        json_str =  dataParsing(data)
                                        msg = str(json_str)  
                                    else:
                                        json_str =  data                                    
                                                                   
                                    DebugLog('','Get message from file!! ','GetBpmFomFile' ,'1') 
                                    parseStore(json_str) 
                                except Exception as error :
                                    DebugLog(msg,str(error), 'BPMToPortalFail','0') 
                                else:
                                    print (ifileBpmcount, "sfileBpmList:"+str(len(sfileBpmList)), json_str)                                  
                        # if ifileBpmList < len(sfileBpmList)-1 and bopenfile == True:
                        #     if os.path.exists(src_file_path):
                        #         os.remove (src_file_path)
                        #     os.rename (dst_file_path, src_file_path)

if __name__ == "__main__":    
    sourcedata = os.getenv('SOURCE')
    # sourcedata = "bpmJson"
    mainfunction(sourcedata)

