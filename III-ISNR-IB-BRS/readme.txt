sudo apt install python3-pip
pip3 install pika
sudo wget https://ak-delivery04-mul.dhe.ibm.com/sdfdl/v2/sar/CM/WS/086t9/0/Xa.2/Xb.jusyLTSp44S0eZU4L_Z8CxT9s111g6PLY3eV4pG5FjCmcyQcWmWZ1ZOteYw/Xc.CM/WS/086t9/0/9.1.0.2-IBM-MQC-UbuntuLinuxX64.tar.gz/Xd./Xf.LPR.D1VK/Xg.10174485/Xi.habanero/XY.habanero/XZ.aTYAtx6Ht3WYPrMxQwoSSSgiXys/9.1.0.2-IBM-MQC-UbuntuLinuxX64.tar.gz
mkdir IBMMQC
sudo tar -xvf 9.1.0.2-IBM-MQC-UbuntuLinuxX64.tar.gz -C ~/IBMMQC
cd ./IBMMQC
sudo ./mqlicense.sh -accept
sudo dpkg -i ibmmq-runtime_9.1.0.2_amd64.deb
sudo dpkg -i ibmmq-client_9.1.0.2_amd64.deb 
sudo dpkg -i ibmmq-sdk_9.1.0.2_amd64.deb 
pip3 install pymqi
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mqm/lib64/
