from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import argparse

CONNECTION_STR = os.environ.get('SERVICE_BUS_CONN_STR')
QUEUE_NAME = "pendingPrompts"

def send_messages_to_queue(num_messages):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

    with open("azure-services.txt", "r") as f:
        services = f.readlines()

    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            count = 0  
            for service in services:
                if count >= num_messages:
                    break
                service = service.strip()  
                message = ServiceBusMessage(f"Write a 100-word love poem about {service}")
                sender.send_messages(message)
                print(f"Sent message {count+1} for {service}")
                count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send messages to Azure Service Bus queue')
    parser.add_argument('num_messages', type=int, help='Number of messages to send')
    args = parser.parse_args()
    send_messages_to_queue(args.num_messages)