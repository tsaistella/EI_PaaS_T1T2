export RABBITMQ_USER="isnr"
export RABBITMQ_PASSWORD="isnr2019"
export RABBITMQ_HOST="172.20.0.220"
export RABBITMQ_PORT="5671"
export RABBITMQ_VHOST="isnr"
export RABBITMQ_BPMEXCHANGE="bpm"
export RABBITMQ_QUEUENAME="bpm"
export RABBITMQ_ROUTING_KEY="bpm_rk"
export PORTAL_URL="http://127.0.0.1:8000/baggages/api/v1/bpm/"
export PORTAL_TOKEN="3e74e351fb4096af14c9e318af2f5bffed6fba2c"
python storedata.py
