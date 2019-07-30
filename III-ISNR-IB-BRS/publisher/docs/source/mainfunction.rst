主流程程式說明
================

.. automodule:: fetchdata
   :members: mainfunction 

.. automodule:: fetchdata
   :members: DebugLog 


|

    BRS-ib-publisher 透過API將系統運作的稽核記錄，發至Portal Server,其EvenLog種類說明，列表如下:

    =====================  =================================================================================================
    Event Log 種類          事件狀況說明
    =====================  =================================================================================================
    MqConnectSucces        成功連接IBMMQ Server。
    MqConnectFail          連接IBMMQ Server 失敗。
    GetMesFormIbmMQ        成功從IBMQ Server取得BPM資訊。
    BpmToRabbbitMQ         成功推送BPM資訊到RabbitMQ Server
    RabbitMqError          與RabbitMQ Server之間出現異常，無法成功推送BPM資訊
    IbmMQException         從IBMMQ Server中取得BPM資訊時，出現例外狀況，包括資訊為空或連線被中斷等等…非成功獲得BPM資訊的例外情況。
    IbmMqClose             發出與IBMMQ Server通道關閉的請求。
    IbmMqDisconnect        發出與IBMMQ Server斷線的請求。
    =====================  =================================================================================================

|