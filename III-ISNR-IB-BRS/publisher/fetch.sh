export RABBITMQ_USER="isnr"
export RABBITMQ_PASSWORD="isnr2019"
export RABBITMQ_HOST="172.20.0.220"
export RABBITMQ_PORT="5671"
export RABBITMQ_VHOST="isnr"
export RABBITMQ_BPMEXCHANGE="bpm"
export RABBITMQ_QUEUENAME="bpm"
export RABBITMQ_ROUTING_KEY="bpm_rk"
export LD_LIBRARY_PATH="/opt/mqm/lib64/"
export IBMQUEUE_MANAGER="TIABPM"
export IBMCHANNEL="TAISNR.SVRCONN"
export IBMHOST="10.2.67.76"
export IBMPORT="1414"
export IBMQUEUE_NAME="TAISNR.LOCAL.QUEUE"
export IBMUSER="TAISNRBPM"
export IBMPASSWORD="Taisnr123456!"
export DebugLog="Open"
export FailToSleepSec="20"
export DisconnectSec="600"
export PORTALLOG_URL="http://172.20.0.228:5555/common/api/v1/apilog/"
export PORTAL_TOKEN="0d7bb5e553351702b633ccfe46c93fa007f6e4f1"
python3 ./code/fetchdata.py
