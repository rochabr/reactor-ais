from azure.servicebus import ServiceBusClient

import os

CONNECTION_STR = os.environ["SERVICEBUS_CONN_STR"]
QUEUE_NAME = os.environ["QUEUE_NAME"]

with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
    # max_wait_time specifies how long the receiver should wait with no incoming messages before stopping receipt.
    # Default is None; to receive forever.
    with client.get_queue_receiver(QUEUE_NAME, max_wait_time=30) as receiver:
        for msg in receiver:  # ServiceBusReceiver instance is a generator.
            print(str(msg))
            # receiver.complete_message(msg)
            # If it is desired to halt receiving early, one can break out of the loop here safely.
