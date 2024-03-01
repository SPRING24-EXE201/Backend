import json

from azure.servicebus import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from exe201_backend import settings
from exe201_backend.common.constants import SystemConstants
from exe201_backend.common.cosmosDB.access import CosmosDBAccess


class ServiceBus:
    servicebus_client = ServiceBusClient.from_connection_string(
            conn_str=settings.SERVICE_BUS_CON,
            logging_enable=True)


def send_single_message(sender, message, authorization_key):
    message_svb = ServiceBusMessage(json.dumps(message), content_type='application/json')
    if authorization_key:
        message_svb.application_properties = {
            'Authorization': authorization_key
        }
    # send the message to the topic
    sender.send_messages(message_svb)


def handler_message(message, config_type, controller_id=None):
    config = CosmosDBAccess.get_config(controller_id, config_type)
    if not config:
        raise ValueError('Không tìm thấy thông tin config')

    # Get a Topic Sender object to send messages to the topic
    sender = ServiceBus.servicebus_client.get_topic_sender(topic_name=config.topic_name)
    with sender:
        # Send one message
        send_single_message(sender=sender, message=message, authorization_key=config.authorization_key)
