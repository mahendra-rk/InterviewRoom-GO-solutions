import ibm_mq
import json

conn_info = {
    "queue_manager": "QMGR",
    "channel": "CHANNEL",
    "host": "localhost",
    "port": "1414",
    "ssl_cipher_spec": "TLS_RSA_WITH_AES_256_CBC_SHA256",
    "auth_type": "MQCSP_AUTH_NONE"
}

queue_manager = conn_info["queue_manager"]
channel = conn_info["channel"]
host = conn_info["host"]
port = conn_info["port"]
auth_type = conn_info["auth_type"]
ssl_cipher_spec = conn_info["ssl_cipher_spec"]

sco = ibm_mq.MQSCO()
sco.KeyRepository = "/var/ssl/key"
sco.SSLCipherSpec = ssl_cipher_spec
cd = ibm_mq.MQCSP()
cd.AuthenticationType = ibm_mq.MQCSP_AUTH_NONE

qmgr = ibm_mq.MQQueueManager(queue_manager, cd=cd, channel=channel, conn="tcp://" + host + "(" + port + ")", ssl=sco)

queue_name = "QUEUE_NAME"
queue = ibm_mq.MQQueue(qmgr, queue_name, ibm_mq.MQOO_INPUT_SHARED)

message_desc = ibm_mq.MQMD()
message_options = ibm_mq.MQGMO()
message_options.Options = ibm_mq.MQGMO_WAIT | ibm_mq.MQGMO_FAIL_IF_QUIESCING
message_options.WaitInterval = 5000

def run():
    for i in range(1000):
        try:
            message = queue.get(None, message_desc, message_options)
            message_body = message.decode("utf-8")
            print(message_body)
            
        except ibm_mq.MQMIError as e:
            if e.comp == ibm_mq.MQCC_FAILED and e.reason == ibm_mq.MQRC_NO_MSG_AVAILABLE:
                continue
                print("running counter : " + i)
            else:
                raise e

def close():
    queue.close()
    qmgr.disconnect()
    
