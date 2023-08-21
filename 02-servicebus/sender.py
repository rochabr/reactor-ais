from azure.servicebus import ServiceBusClient, ServiceBusMessage

import os

connstr = os.environ["SERVICEBUS_CONN_STR"]
queue_name = os.environ["SERVICE_BUS_QUEUE_NAME"]

with ServiceBusClient.from_connection_string(connstr) as client:
    with client.get_queue_sender(queue_name) as sender:
        # Sending a single message
        single_message = ServiceBusMessage("Single message")
        sender.send_messages(single_message)

        # Sending a list of messages
        messages = [
            ServiceBusMessage("First message"),
            ServiceBusMessage("Second message"),
        ]
        sender.send_messages(messages)
