# Create Azure resources

1. Clone the repo locally
2. Run
   ```bash
   cd reactor-ais/02-servicebus
   ```
3. Update _infra.azcli_ with your resource group name, namespace name, location and queue name.
4. Run
   ```bash
   . infra.cli
   ```
After the environment is created, move to the next step.

# Setup Python environment and files

## Setup Connection String

```bash
export SERVICEBUS_CONN_STR=$(az servicebus namespace authorization-rule keys list --resource-group $RESOURCE_GROUP --namespace-name $NAMESPACE_NAME --name RootManageSharedAccessKey --query primaryConnectionString --output tsv)
export QUEUE_NAME=$QUEUE_NAME
```

## Install dependencies

```bash
pip install azure-servicebus
```

## Create sender.py

```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage

import os

connstr = os.environ["SERVICEBUS_CONN_STR"]
queue_name = os.environ["QUEUE_NAME"]

with ServiceBusClient.from_connection_string(connstr) as client:
    with client.get_queue_sender(queue_name) as sender:
        # Sending a single message
        single_message = ServiceBusMessage("Hello, Reactor!")
        sender.send_messages(single_message)

        # Sending a list of messages
        messages = [
            ServiceBusMessage("Day 1 - Logic Apps"),
            ServiceBusMessage("Day 2 - Service Bus"),
        ]
        sender.send_messages(messages)
```

## Create receiver.py

```python
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

```

# Running the demo

First, run *sender.py* to send messages to the queue.

```bash
python sender.py
```

Then, run *receiver.py* to receive messages from the queue.

```bash
python receiver.py
```

On the Azure Portal, open your Azure Service bus instance and Queue. Navigate to _Service Bus Explorer_ to see the messages being consumed and sent in real-time.

# Cleanup resources
```bash
az group delete --name $RESOURCE_GROUP
```
