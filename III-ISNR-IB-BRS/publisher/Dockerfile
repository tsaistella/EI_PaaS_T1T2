FROM ubuntu:18.04

RUN sed -i 's/archive\.ubuntu\.com/tw.archive.ubuntu.com/g' /etc/apt/sources.list

RUN apt-get clean && apt-get update && apt-get -y install python3 python3-pip

ADD ./9.1.0.2-IBM-MQC-UbuntuLinuxX64.tar.gz /IBMMQC  
RUN  ./IBMMQC/mqlicense.sh -accept
RUN dpkg -i ./IBMMQC/ibmmq-runtime_9.1.0.2_amd64.deb  \
  &&  dpkg -i ./IBMMQC/ibmmq-client_9.1.0.2_amd64.deb  \
  &&  dpkg -i ./IBMMQC/ibmmq-sdk_9.1.0.2_amd64.deb 

# Ensure UTF-8 locale
#COPY locale /etc/default/locale
RUN apt-get install locales
RUN locale-gen en_US.UTF-8 &&\
  DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:zh  
ENV LC_ALL en_US.UTF-8  

ENV RABBITMQ_USER=isnr
ENV RABBITMQ_PASSWORD=isnr2019
ENV RABBITMQ_HOST=172.20.0.220
ENV RABBITMQ_PORT=5671
ENV RABBITMQ_VHOST=isnr
ENV RABBITMQ_BPMEXCHANGE=bpm
ENV RABBITMQ_QUEUENAME=bpm
ENV RABBITMQ_ROUTING_KEY=bpm_rk
ENV LD_LIBRARY_PATH=/opt/mqm/lib64/
ENV IBMQUEUE_MANAGER=TIABPM
ENV IBMCHANNEL=TAISNR.SVRCONN
ENV IBMHOST=10.2.67.76
ENV IBMPORT=1414
ENV IBMQUEUE_NAME=TAISNR.LOCAL.QUEUE
ENV IBMUSER=TAISNRBPM
ENV IBMPASSWORD=Taisnr123456!
ENV DebugLog=Open
ENV FailToSleepSec=20
ENV DisconnectSec=600
ENV PORTALLOG_URL=http://172.20.0.228:5555/common/api/v1/apilog/
ENV PORTAL_TOKEN=0d7bb5e553351702b633ccfe46c93fa007f6e4f1

WORKDIR /app  
ADD . /app  
RUN pip3 install -r requirements.txt
CMD ["bash", "fetch.cmd"]  
 
