import pymqi 

class IBMMQClientManager(object):
    def __init__(self, queue_manager, channel, host, port, queue_name, conn_info):
        self.queue_manager = queue_manager
        self.channel = channel
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.conn_info = conn_info

    def connect(self, user, password):  
        """
        connect
		與IBM MQ Server建立連線。
        """
        pymqi.queue_manager = self.queue_manager
        pymqi.channel = self.channel
        pymqi.host = self.host
        pymqi.port = self.port
        pymqi.queue_name = self.queue_name
        pymqi.conn_info = self.conn_info        
        self.user = user
        self.password = password
        self.qmgr = pymqi.connect(self.queue_manager, self.channel, self.conn_info,  user,  password)
        

    def Queue(self): 
        """
        Queue
        宣告挷定佇列
        """
        self.ibmqueue = pymqi.Queue(self.qmgr, self.queue_name)
        
    def getmessage(self):
        """
        getmessage
        取得佇列中的資訊
        """
        return self.ibmqueue.get().decode('utf-16')
      
    def close(self): 
        """
        close        
        關閉佇列
        """       
        self.ibmqueue.close()    
   
    def disconnect(self): 
        """
        disconnect        
		切斷與IBM MQ Server的連線。
        """  
        self.qmgr.disconnect()
    
    def is_connected(self): 
        """
        is_connected
		判斷與IBM MQ Server的連線狀況。
        """       
        return self.qmgr._is_connected()

    

