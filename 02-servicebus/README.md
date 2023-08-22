# Create resource group 

```bash
az group create --name reactor-servicebus-rg --location eastus
```

# Create namespace

```bash
az servicebus namespace create --resource-group reactor-servicebus-rg --name reactor-demo-sbus --location eastus
```

# Create queue
```bash
az servicebus queue create --resource-group reactor-servicebus-rg --namespace-name reactor-demo-sbus --name orders-queue
```

# Setup Connection String and Queue name

```bash
RES_GROUP=reactor-servicebus-rg
NAMESPACE_NAME=reactor-demo-sbus

export SERVICEBUS_CONN_STR=$(az servicebus namespace authorization-rule keys list --resource-group $RES_GROUP --namespace-name $NAMESPACE_NAME --name RootManageSharedAccessKey --query primaryConnectionString --output tsv)

export SERVICE_BUS_QUEUE_NAME=orders-queue
```

# Install dependencies

```bash
pip install azure-servicebus
```

## Create sender.py

```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage

import os

connstr = os.environ["SERVICEBUS_CONN_STR"]
queue_name = os.environ["SERVICE_BUS_QUEUE_NAME"]

with ServiceBusClient.from_connection_string(connstr) as client:
    with client.get_queue_sender(queue_name) as sender:
        # Sending a single message
        single_message = ServiceBusMessage("Hello, Reactor!")
        sender.send_messages(single_message)

        # Sending a list of messages
        messages = [
            ServiceBusMessage("Day 1 - Logic Apps"),
            ServiceBusMessage("Da 2 - Service Bus"),
        ]
        sender.send_messages(messages)
```

## Create receiver.py

```python
from azure.servicebus import ServiceBusClient

import os

connstr = os.environ["SERVICEBUS_CONN_STR"]
queue_name = os.environ["SERVICE_BUS_QUEUE_NAME"]

with ServiceBusClient.from_connection_string(connstr) as client:
    # max_wait_time specifies how long the receiver should wait with no incoming messages before stopping receipt.
    # Default is None; to receive forever.
    with client.get_queue_receiver(queue_name, max_wait_time=30) as receiver:
        for msg in receiver:  # ServiceBusReceiver instance is a generator.
            print(str(msg))
            # receiver.complete_message(msg)
            # If it is desired to halt receiving early, one can break out of the loop here safely.

```