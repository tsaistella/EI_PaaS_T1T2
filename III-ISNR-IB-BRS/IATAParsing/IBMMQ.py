import pymqi

queue_manager = "TIABPM"
channel = "TAISNR.SVRCONN"
host = "10.2.67.76"
port = "1414"
queue_name = "TAISNR.LOCAL.QUEUE"
message = "Hello from Python!"
conn_info = "%s(%s)" % (host, port)

# Message Descriptor
md = pymqi.MD()

# Get Message Options
gmo = pymqi.GMO()
gmo.Options = pymqi.CMQC.MQGMO_WAIT | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
gmo.WaitInterval = 5000 # 5 seconds

qmgr = pymqi.connect(queue_manager, channel, conn_info)
queue = pymqi.Queue(qmgr, queue_name)

keep_running = True

while keep_running:
    try:
        # Wait up to to gmo.WaitInterval for a new message.
        message = queue.get(None, md, gmo)

        # Process the message here..

        # Reset the MsgId, CorrelId & GroupId so that we can reuse
        # the same 'md' object again.
        md.MsgId = pymqi.CMQC.MQMI_NONE
        md.CorrelId = pymqi.CMQC.MQCI_NONE
        md.GroupId = pymqi.CMQC.MQGI_NONE

    except pymqi.MQMIError, e:
        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
            # No messages, that's OK, we can ignore it.
            pass
        else:
            # Some other error condition.
            raise

queue.close()
qmgr.disconnect()