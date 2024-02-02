from azure.servicebus import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from exe201_backend import settings
from exe201_backend.common.constants import SystemConstants


def send_single_message(sender, message):
    # send the message to the topic
    sender.send_messages(ServiceBusMessage(message))
    return None


def handler_message(message, topic):
    try:
        NAMESPACE_CONNECTION_STR = settings.SERVICE_BUS_CON
        with ServiceBusClient.from_connection_string(
            conn_str=NAMESPACE_CONNECTION_STR,
            logging_enable=True,
            ) as servicebus_client:
            # Get a Topic Sender object to send messages to the topic
            sender = servicebus_client.get_topic_sender(topic_name=topic)
            with sender:
                # Send one message
                send_single_message(sender, message = message)
    except Exception as e:
        data = e.message
    return None
