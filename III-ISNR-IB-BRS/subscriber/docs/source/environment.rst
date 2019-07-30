環境安裝設定與佈置
==================

|
 
**RabbitMQ套件安裝 ：**
 應用程式需事先安裝\ **pika**\套件，以\ **AMQP**\的方法, 運用\ **綁定**\佇列與RabbitMQ伺服器機器進行連接通訊。
 
 RabbitMQ pika套件安裝:
  在命令列(CMD)中, 執行:
  "pip install pika" 或 "pip install -r requirements.txt" (pika已列表於requirements.txt中)。

|
|

**Web requests套件安裝 ：**
 應用程式需事先安裝\ **requests**\套件，進行透過呼叫 Portal API 將資料儲存至機場營運數據庫。
 
 Web requests套件安裝:
  在命令列(CMD)中, 執行:
  "pip install requests" 或 "pip install -r requirements.txt" (requests已列表於requirements.txt中)。

|
|



**執行環境佈署：**
 將程式包裝成 CF App 形式並佈署。
    在命令列(CMD)中, 執行:

     (1) 切換到subscriber程式資料夾中。

     (2) cf push -b python_buildpack_offline -c "bash store.cmd"。
   
