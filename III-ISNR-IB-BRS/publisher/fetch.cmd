export RABBITMQ_USER="isnr"
export RABBITMQ_PASSWORD="isnr2019"
export RABBITMQ_HOST="172.20.0.220"
export RABBITMQ_PORT="5671"
export RABBITMQ_VHOST="isnr"
export RABBITMQ_BPMEXCHANGE="bpm"
export RABBITMQ_QUEUENAME="bpm"
export LD_LIBRARY_PATH="/opt/mqm/lib64/"
export IBMQUEUE_MANAGER="TIABPM"
export IBMCHANNEL="TAISNR.SVRCONN"
export IBMHOST="10.2.67.76"
export IBMPORT="1414"
export IBMQUEUE_NAME="TAISNR.LOCAL.QUEUE"
export IBMUSER="TAISNRBPM"
export IBMPASSWORD="Taisnr123456!"
export IBMROUTING_KEY="bpm_rk"
python3 fetchdata.py