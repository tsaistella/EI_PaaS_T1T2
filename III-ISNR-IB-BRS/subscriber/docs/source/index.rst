.. BRS-ib-subscriber documentation master file, created by
   sphinx-quickstart on Tue Jun 18 14:32:33 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BRS-ib-subscriber
##################

**功能：** 
 
 從 RabbitMQ 取得BPM原始文字格式資料，進行Parse 來源之 BPM 格式資料且轉化格式為JSON，透過呼叫 Portal API 將資料儲存至機場營運數據庫。
 
 ..  image:: img/9.png
    :height: 350
    :width: 637

|
|

**IATA 行李訊息：** 

    \ **(一) 行李訊息種類介紹**\
     
     國際航空運輸協會(英語：International Air Transport Association，縮寫IATA)，將行李的資訊訂定分為八大種類，運用於航務行李系統彼此之間，有關行李在各種情境狀況的資訊溝通與航運處理。如下表：

     ..  image:: img/1.png
         :height: 800
         :width: 835
 
     舉例說明，如：一名轉機旅客從美國甘迺迪國際機場(IATA代碼：JFK)起飛, 在德國法蘭克福機場(IATA代碼：FRA)進行轉機，飛往新加坡樟宜機場(IATA代码：SIN)。該名旅客的行李原始資訊(BSM)及行李處理資訊(BPM), 會被登入在行李作業系統(BHS－Baggage Handling System)與機場出境控管系統(DCS－Departure Control System)，進行行李資訊的轉交溝通。此其之外，機場出境控管系統(DCS－Departure Control System)，需要再提供轉機的行李轉移資訊(BTM)。

     ..  image:: img/2.png
         :height: 319
         :width: 550
 
| 

    \ **(二) BPM與BSM 格式簡介**\
     
     旅客在check-in行李時，系統會自動將出入境飛航資訊，行李條碼，旅客個人資料，以及攜帶的行李大小重量等相關的資訊，編譯生產一組依國際標準格式的行李原始資訊(BSM)，再經由地勤人員掃條碼裝櫃，觸發後端系統將行李原始資訊(BSM)，加入裝櫃資訊(.U .Q)及程序資訊(.J)，生成行李處理資訊(BPM)。下圖為標準格式的呈現，一組完整的行李處理資訊(BPM)，起始識別碼為”BPM”，結尾識別碼為”ENDBPM”，各元素類型以”.”為區分，內文資訊用”/”分割，如：出境資訊：.F/BA117/030CT/SEL/J。

     ..  image:: img/3.png
         :height: 402
         :width: 595
 
     以數學表示BSM和BPM之間的關係，如下

     ..  image:: img/4.png
         :height: 68
         :width: 120
 
| 

    \ **(三) 實作IATA　BPM/BSM 解析器**\
     
     採用高度擴充的程式設計架構，進行實作IATA行李資訊的解析器，擴充未來規格書的變更及容納更多的行李資訊種類。在程式資料結構中，按照規格書規範，順序列出所定義的元素及內文，程式解析器會動態解析原始行李資訊，以JSON格式的呈現，讓後端程式，可快速加以運用。
     
     以擴充行李管理資訊(BCM)為範例，管理者參考規格書和元素內文列表之間的差異，如下圖紅色矩形範圍的部份是BCM與BPM差異新增的元素內文：

     ..  image:: img/5.png
         :height: 271
         :width: 640
              
     依序列出新增差異的部份，如下圖紅色字體的新增：
     
     ..  image:: img/6.png
         :height: 616
         :width: 960
              
     程式將會自動動態擴充加入的行李管理資訊(BCM)格式，同時保留支援原先已加入的BPM, BSM, BTM等行李資訊種類，執行結果如下圖：
     
     ..  image:: img/7.png
         :height: 200
         :width: 510

| 

    \ **(四) 創建行李資訊的主鍵**\
     
     在行李識別碼上，國際航空運輸協會(IATA)創建唯一識別的行李條碼。但機場實際操作上，會間隔一段時間後，重複使用過往的行李條碼，只保證當下行李條碼不重複，系統不會追溯過往行李條碼是否有被使用過，這有可能造成，運用歷史BPM資訊的其他系統，遇到行李條碼衝突的問題。因此額外創建行李資訊的主鍵，預防此狀況，實作如下圖：
     
     ..  image:: img/8.png
         :height: 663
         :width: 930  

|
|

**環境安裝設定與佈置:**
 
 **RabbitMQ套件安裝 ：**
  應用程式需事先安裝\ **pika**\套件，以\ **AMQP**\的方法, 運用\ **綁定**\佇列與RabbitMQ伺服器機器進行連接通訊。

  RabbitMQ pika套件安裝:
   在命令列(CMD)中, 執行:
   "pip install pika" 或 "pip install -r requirements.txt" (pika已列表於requirements.txt中)。

|

 **Web requests套件安裝 ：**
  應用程式需事先安裝\ **requests**\套件，進行透過呼叫 Portal API 將資料儲存至機場營運數據庫。

  Web requests套件安裝:
   在命令列(CMD)中, 執行:
   "pip install requests" 或 "pip install -r requirements.txt" (requests已列表於requirements.txt中)。

|

 **執行環境佈署：**
  將程式包裝成 CF App 形式並佈署。
  在命令列(CMD)中, 執行:
   
   (1) 切換到subscriber程式資料夾中。
   
   (2) cf push -b python_buildpack_offline -c "bash store.cmd"。

|
|

**程式控制與驗證:**
 
 **啟動應用程式：**
   在命令列(CMD)中, 執行"cf start brs-ib-subscriber"
   
    ..  image:: img/10.png
        :height: 200
        :width: 600
            
|

 **關閉應用程式：**
   在命令列(CMD)中, 執行"cf stop brs-ib-subscriber"
   
    ..  image:: img/11.png
        :height: 40
        :width: 600

|

 **執行結果驗證：**
  
  (1) 驗證是否成功取得，來自RabbitMQ佇列中的BPM資訊。
      查看已接收的BPM資訊內容和時戳，如下圖範例:
     
         ..  image:: img/12.png
             :height: 500
             :width: 900
  
   
  (2) 驗證BRS-ib-subscriber，將BPM資訊，透過呼叫 Portal API 將資料儲存至機場營運數據庫。
 
         ..  image:: img/13.png
             :height: 280
             :width: 545
 

|
|
 
**環境參數設定值：** 
 
    =====================  ===================  =======================================================
    RabbitMQ 參數名稱       參數值               功能
    =====================  ===================  =======================================================
    RABBITMQ_USER          isnr                 使用者帳號
    RABBITMQ_PASSWORD      isnr2019             使用者密碼
    RABBITMQ_HOST          172.20.0.220         連接 MQ Server 的網路位置(IP)
    RABBITMQ_PORT          5671                 連接 MQ Server 的連接埠
    RABBITMQ_VHOST         isnr                 連接 MQ Server 的主機名
    RABBITMQ_BPMEXCHANGE   bpm                  連接 MQ Server 的交換機名稱
    RABBITMQ_QUEUENAME     bpm                  連接 MQ Server 的佇列名稱
    RABBITMQ_ROUTING_KEY   bpm_rk               連接 MQ Server 的挷定鍵。交換機利用挷定鍵，挷定指定的佇列  
    =====================  ===================  =======================================================

|

    =====================  ================================================  =========================
    portal 參數名稱          參數值                                             功能
    =====================  ================================================  =========================
    PORTAL_URL              http://172.20.0.228:5555/baggages/api/v1/bpm/    連接 portal 的網址
    PORTAL_TOKEN            3e74e351fb4096af14c9e318af2f5bffed6fba2c         連接 PORTportalAL 的標記
    =====================  ================================================  =========================
    
|
|

**開發過程備註:** 

    \ **有多少情境會產生BPM/BSM透過IBMMQ傳到後台??(類型)**\
     確認目前機場只有打櫃的BPM資訊。

     確認目前一組行李條碼會產生一個打櫃BPM資訊 (1:1)      

    \ **哪些情境需要處理?(篩選)ALL?**\
     機場要求，提出一個設計規範，說明可支援擴充，所有可能的BPM/BSM資訊類型。

    \ **取得哪些有意議的資訊?(萃取)**\
     全部資訊均要被完整保留


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   function
   IATA 
   environment
   control
   parameter
   mainfunction
   IATAParsing
   QueueManager
   WebRequestManager
   portalLog
   note




