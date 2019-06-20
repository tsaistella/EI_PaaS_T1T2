程式控制與驗證
=================

|

**啟動應用程式：**
 \ **Windows**\:
  在命令列(CMD)中, 執行"fetchVS.cmd"

 \ **Linux**\:
  "sh fetch.sh"
  
 \ **Docker Image**\:
   首次建立並執行: "docker run -d –name brs-publisher brspublisher"

   啟動已建立的Docker: "docker start brs-publiser"

|
|

**關閉應用程式：**
 \ **Windows**\:
  在執行"fetchVS.cmd"的命令列(CMD)中, 輸入Ctrl+C中止指令

 \ **Linux**\:
  在執行"sh fetch.sh"的bash命令列中, 輸入Ctrl+C中止指令
  
 \ **Docker Image**\:
   關閉執行中的Docker: "docker stop brs-publiser"

|
|

**執行結果驗證：**
 (1) 驗證是否成功取得，來自IBM MQ Server 佇列中的BPM資訊。
     開啟除錯模式(DebugLog=Open)後，在程式執行目錄中的DebugLog資料夾，可查看已接收的BPM資訊內容和時戳，如下圖範例:
    
        ..  image:: img/7.png
            :height: 242
            :width: 241
     
     記錄分為兩種資訊:(1)包含BPM及連線狀態的所有資訊，格式:BPM_西元年-月-日.txt  (2)僅有連線狀態的資訊，格式:Connect_西元年-月-日.txt。
    
        ..  image:: img/8.png
            :height: 35
            :width: 316
         
     若是Docker佈置的環境下，可執行"\ **docker exec -it brs-publisher bash**\"，進入程式執行目錄中，再切換進入DebugLog資料夾，查看接收記錄。
     
     若是Windows或Linux的環境下，進入程式執行目錄中，再切換進入DebugLog資料夾，查看接收記錄。

|
       
 (2) 驗證BRS-ib-publisher，可將BPM資訊成功的推送到RabbitMQ的BPM佇列中。

     (1) 執行"\ **cf stop brs-ib-subscriber**\", 將Sbuscriber關閉，停止訂閱RabbitMQ BPM佇列中的BPM資訊。

     (2) 參考"\ **啟動應用程式**\"章節，進行啟動brs-publisher。以\ **Docker Image**\為佈置環境，請執行"\ **docker run -d --name brs-publisher brspublisher**\"

     查看佇列中的總個數是否增多，來進行驗證推送功能是否正常。如下圖，隨著時間拉長，BPM佇列中的BPM資訊總個數不斷增加。

        ..  image:: img/6.png
            :height: 556
            :width: 1090
