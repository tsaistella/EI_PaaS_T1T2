主流程程式說明
================

.. automodule:: storedata
   :members: mainfunction 

.. automodule:: storedata
   :members: dataParsing 

.. automodule:: storedata
   :members: parseStore 


.. automodule:: storedata
   :members: DebugLog 


|

    BRS-ib-subscriber 透過API將系統運作的稽核記錄，發至Portal Server,其EvenLog種類說明，列表如下:

    =====================  ====================================================================================
     Event Log 種類          事件狀況說明
    =====================  ====================================================================================
     BPMtoPORTAL            成功傳送解析後的BPM資訊至PORTAL Server。
     source:RabbitMQ        來源是從RabbitMQ Server中取得未Parse語意過的BPM資訊。
     source:bpmOrg          來源是從文件中取得未Parse語意過的BPM資訊。
     source:bpmJson         來源是從文件中取得已Parse語意過的BPM資訊。
     GetBpmFomMQ            成功從RabbitMQ Server取得BPM資訊，count=1:取得BPM資訊。
     GetBpmFomMQFAIL        從RabbitMQ Server取得BPM資訊異常例外狀況的失敗。
     WaitBpmMsg             此時佇列為空，系統持續監聽RabbitMQ Server佇列。
     Alert_MqFail           系統與RabbitMQ Server發生連線的異常例外狀況。
     FileNotFound           來源資件夾 "SourceLog" 中沒有檔案。(source:bpmOrg 和　source:bpmJson從檔案中讀取BPM)
     MakedirFail            系統建立 "DoneLog" 資訊夾時，發生失敗。
     Alert_pathError        讀取BPM文件檔失敗。
     GetBpmFomFile          成功從文件中取得BPM資訊，count=1:取得BPM資訊。
     BPMToPortalFail        將解析後的BPM傳至Portal時，發生異常失敗狀況。
    =====================  ====================================================================================

|