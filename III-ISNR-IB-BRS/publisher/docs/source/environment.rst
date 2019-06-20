環境安裝設定與佈置
==================

|
 
**IBMMQ 用戶端角色設定與軟體安裝 ：**
 以\ **應用程式（MQI 用戶端）**\的方式, 使用\ **雙向**\通訊鏈結的\ **MQI 通道 (MQI channel)**\，與伺服器機器上的佇列管理程式進行連接通訊。

        ..  image:: img/2.png
            :height: 162
            :width: 345


 應用程式（MQI 用戶端）, 必需先安裝\ **IBM-MQC**\，再使用pymqi套件與IBM Server連接傳訊。

 IBM-MQC 下載版本及安裝流程 (\ **Windows**\):
    (1) 安裝9.1.2.0-IBM-MQC-Win64\Windows\Setup.exe
    (2) 安裝vs_buildtools__299754906.1551855808.exe
    (3) 在命令列(CMD)中, 執行"pip install pymqi" 或 “pip install -r requirements.txt” (pymqi已列表於requirements.txt中)。

        ..  image:: img/10.png
            :height: 55
            :width: 132

|

 IBM-MQC 下載版本及安裝流程(\ **Linux**\):
    (1) sudo wget https://ak-delivery04-mul.dhe.ibm.com/sdfdl/v2/sar/CM/WS/086t9/0/Xa.2/Xb.jusyLTSp44S0eZU4L_Z8CxT9s111g6PLY3eV4pG5FjCmcyQcWmWZ1ZOteYw/Xc.CM/WS/086t9/0/9.1.0.2-IBM-MQC-UbuntuLinuxX64.tar.gz/Xd./Xf.LPR.D1VK/Xg.10174485/Xi.habanero/XY.habanero/XZ.aTYAtx6Ht3WYPrMxQwoSSSgiXys/9.1.0.2-IBM-MQC-UbuntuLinuxX64.tar.gz
    (2) mkdir IBMMQC
    (3) sudo tar -xvf 9.1.0.2-IBM-MQC-UbuntuLinuxX64.tar.gz -C ./IBMMQC
    (4) cd ./IBMMQC
    (5) sudo ./mqlicense.sh –accept
    (6) sudo dpkg -i ibmmq-runtime_9.1.0.2_amd64.deb
    (7) sudo dpkg -i ibmmq-client_9.1.0.2_amd64.deb 
    (8) sudo dpkg -i ibmmq-sdk_9.1.0.2_amd64.deb 
    (9) sudo apt install python3-pip
    (10) "pip3 install pymqi" 或 "pip install -r requirements.txt" (pymqi已列表於requirements.txt中)。
    (11) export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mqm/lib64/    

|

 IBM-MQC 下載版本及安裝流程(\ **Docker Image**\):
    參考"執行環境佈署"章節，將程式打包成 Docker Image 形式佈署的指令，即可自動安裝IBM-MQC的軟體及pymqi套件。
     Dockerfile中有關IBM-MQC軟體的列表:

        ..  image:: img/9.png
            :height: 95
            :width: 447
    
     Dockerfile檔:"RUN pip3 install -r requirements.txt"。

|
|

**RabbitMQ套件安裝 ：**
 應用程式需事先安裝\ **pika**\套件，以\ **AMQP**\的方法, 運用\ **綁定**\佇列與RabbitMQ伺服器機器進行連接通訊。
 
 RabbitMQ pika套件安裝:
  在命令列(CMD)中, 執行:
  "pip install pika" 或 "pip install -r requirements.txt" (pika已列表於requirements.txt中)。

        ..  image:: img/10.png
            :height: 55
            :width: 132


|
|

**執行環境佈署：**
 將程式打包成Docker Image 形式佈署。
    (1) docker build -t brspublisher .
    
        ..  image:: img/3.png
            :height: 70
            :width: 910

    (2) docker images
    
        ..  image:: img/4.png
            :height: 116
            :width: 1202

    (3) docker run -d --name brs-publisher brspublisher
    
        ..  image:: img/5.png
            :height: 110
            :width: 914
