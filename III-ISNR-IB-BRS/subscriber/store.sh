export RABBITMQ_USER="isnr"
export RABBITMQ_PASSWORD="isnr2019"
export RABBITMQ_HOST="172.20.0.220"
export RABBITMQ_PORT="5671"
export RABBITMQ_VHOST="isnr"
export RABBITMQ_BPMEXCHANGE="bpm"
export RABBITMQ_QUEUENAME="bpm"
export RABBITMQ_ROUTING_KEY="bpm_rk"
export PORTAL_URL="http://172.20.0.228:5555/baggages/api/v1/bpm/"
export PORTAL_TOKEN="0d7bb5e553351702b633ccfe46c93fa007f6e4f1"
export PORTALLOG_URL="http://172.20.0.228:5555/common/api/v1/apilog/"
export DebugLog="Open"
export SOURCE="RabbitMQ"
python ./code/storedata.py
