from azure.servicebus import ServiceBusClient

import os

connstr = os.environ["SERVICEBUS_CONN_STR"]
queue_name = os.environ["QUEUE_NAME"]

with ServiceBusClient.from_connection_string(connstr) as client:
    # max_wait_time specifies how long the receiver should wait with no incoming messages before stopping receipt.
    # Default is None; to receive forever.
    with client.get_queue_receiver(queue_name, max_wait_time=30) as receiver:
        for msg in receiver:  # ServiceBusReceiver instance is a generator.
            print(str(msg))
            # receiver.complete_message(msg)
            # If it is desired to halt receiving early, one can break out of the loop here safely.
