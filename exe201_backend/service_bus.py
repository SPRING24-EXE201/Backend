from azure.servicebus import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from exe201_backend import settings
def send_single_message(sender, message):
    # send the message to the topic
    sender.send_messages(ServiceBusMessage(message))
    return None

def handler_message(message):
    try:
        NAMESPACE_CONNECTION_STR = settings.SERVICE_BUS_CON
        TOPIC_NAME = settings.SERVICE_BUS_TOPIC_NAME
        with ServiceBusClient.from_connection_string(
            conn_str=NAMESPACE_CONNECTION_STR,
            logging_enable=True,
            ) as servicebus_client:
            # Get a Topic Sender object to send messages to the topic
            sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
            with sender:
                # Send one message
                send_single_message(sender, message = message)
    except Exception as e:
        data = e.message
    return None