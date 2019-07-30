程式控制與驗證
=================

|

**啟動應用程式：**
  在命令列(CMD)中, 執行"cf start brs-ib-subscriber"
  
   ..  image:: img/10.png
       :height: 200
       :width: 600
            
|
|

**關閉應用程式：**
  在命令列(CMD)中, 執行"cf stop brs-ib-subscriber"
  
   ..  image:: img/11.png
       :height: 40
       :width: 600
            

|
|

**執行結果驗證：**
 (1) 驗證是否成功取得，來自RabbitMQ佇列中的BPM資訊。
     查看已接收的BPM資訊內容和時戳，如下圖範例:
    
        ..  image:: img/12.png
            :height: 500
            :width: 900

|
       
 (2) 驗證BRS-ib-subscriber，將BPM資訊，透過呼叫 Portal API 將資料儲存至機場營運數據庫。

        ..  image:: img/13.png
            :height: 280
            :width: 545
