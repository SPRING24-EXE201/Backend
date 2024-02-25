import json

from azure.servicebus import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from exe201_backend import settings
from exe201_backend.common.constants import SystemConstants
from exe201_backend.common.cosmosDB.access import CosmosDBAccess


def send_single_message(sender, message, authorization_key):
    message_svb = ServiceBusMessage(json.dumps(message), content_type='application/json')
    if authorization_key:
        message_svb.application_properties = {
            'Authorization': authorization_key
        }
    # send the message to the topic
    sender.send_messages(message_svb)


def handler_message(message, config_type, controller_id=None):
    connection_str = settings.SERVICE_BUS_CON
    config = CosmosDBAccess.get_config(controller_id, config_type)
    if not config:
        raise ValueError('Không tìm thấy thông tin config')

    with ServiceBusClient.from_connection_string(
            conn_str=connection_str,
            logging_enable=True,
    ) as servicebus_client:
        # Get a Topic Sender object to send messages to the topic
        sender = servicebus_client.get_topic_sender(topic_name=config.topic_name)
        with sender:
            # Send one message
            send_single_message(sender=sender, message=message, authorization_key=config.authorization_key)
