set RABBITMQ_USER=isnr
set RABBITMQ_PASSWORD=isnr2019
set RABBITMQ_HOST=172.20.0.220
set RABBITMQ_PORT=5671
set RABBITMQ_VHOST=isnr
set RABBITMQ_BPMEXCHANGE=bpm
set RABBITMQ_QUEUENAME=bpm
set RABBITMQ_ROUTING_KEY=bpm_rk
set PORTAL_URL=http://172.20.0.228:5555/baggages/api/v1/bpm/
set PORTAL_TOKEN=0d7bb5e553351702b633ccfe46c93fa007f6e4f1
set PORTALLOG_URL=http://172.20.0.228:5555/common/api/v1/apilog/
set DebugLog=Open
set SOURCE=bpmJson
python code\storedata.py