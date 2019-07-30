# -*- coding: utf-8 -*-
import os, json
import datetime
from WebRequestManager import WebRequestManager as webmgr

class PortalLog(object):
    def __init__(self):
        pass
        
    def sentLog(self, msg, count):
        """
        sentLog
        透過API 將稽查資料傳送至Web Server，且導入連線例外狀況的容錯處理，連續10次傳送失敗，會將傳送內文輸出打印。
        """    
        url = os.getenv('PORTALLOG_URL')
        token = os.getenv('PORTAL_TOKEN')
                
        # #機場
        # url = "http://172.20.0.228:5555/common/api/v1/apilog/"
        # token = "0d7bb5e553351702b633ccfe46c93fa007f6e4f1"

        # #會內
        # url = "http://124.9.14.14:5555/common/api/v1/apilog/"
        # token = "019d09a5b4dc82f96faa2c010d8dee40f794e033"

        sJson = {}
        sJson['name_system'] = 'BRS'
        sJson['name_program'] = 'publisher'
        sJson['time'] = str(datetime.datetime.now())
        sJson['event'] = str(msg)
        sJson['count'] = str(count)
        json_str = sJson
        webmgr_connect = True   
        icount = 1
        while webmgr_connect:
            try:        
                result = webmgr.post_json(url, json_str, token=token)
                if result.status_code != 201:
                    print(result.text)
                    print(json_str)
                webmgr_connect = False 
                print("check"+ str(result.status_code) +result.text)
            except Exception as patherror :
                print(str(patherror))     
                if icount > 9 :
                    print ("JSON：", json_str)
                    webmgr_connect = False  
                icount = icount + 1  
