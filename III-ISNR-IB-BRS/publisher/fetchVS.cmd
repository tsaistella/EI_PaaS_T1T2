set RABBITMQ_USER=isnr
set RABBITMQ_PASSWORD=isnr2019
set RABBITMQ_HOST=172.20.0.220
set RABBITMQ_PORT=5671
set RABBITMQ_VHOST=isnr
set RABBITMQ_BPMEXCHANGE=bpm
set RABBITMQ_QUEUENAME=bpm
set LD_LIBRARY_PATH=/opt/mqm/lib64/
set IBMQUEUE_MANAGER=TIABPM
set IBMCHANNEL=TAISNR.SVRCONN
set IBMHOST=10.2.67.76
set IBMPORT=1414
set IBMQUEUE_NAME=TAISNR.LOCAL.QUEUE
set IBMUSER=TAISNRBPM
set IBMPASSWORD=Taisnr123456!
set IBMROUTING_KEY=bpm_rk
python3 fetchdata.py