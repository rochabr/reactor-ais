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
