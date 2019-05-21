from QueueManager import QueueManagerUri

def init_queue(qm, exchange):
    for api in FOS_API:
        api_name = api['name'].lower()
        routing_key = '{}_rk'.format(api_name)
        queue = '{}_q1'.format(api_name)
        qm.declare_queue_binding(exchange, queue, routing_key)
