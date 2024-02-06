from azure.cosmos import CosmosClient

from exe201_backend import settings
from exe201_backend.common.cosmosDB.controller_config_model import ControllerConfig


class CosmosDBAccess:
    db_uri = settings.COSMOS_DB_URI
    db_key = settings.COSMOS_DB_KEY
    db_name = settings.COSMOS_DB_NAME
    noti_device_container = settings.COSMOS_DB_NOTI_DEVICE_CONTAINER
    service_bus_config_container = settings.COSMOS_DB_SERVICE_BUS_CONFIG_CONTAINER
    client = CosmosClient(db_uri, db_key, consistency_level='Session')
    database = client.get_database_client(db_name)

    @staticmethod
    def get_config(controller_id, config_type):
        container = CosmosDBAccess.database.get_container_client(CosmosDBAccess.service_bus_config_container)
        query_data = container.query_items(
            query='SELECT * FROM c WHERE c.config_type= @config_type and c.controller_id = @controller_id',
            parameters=[dict(name='@config_type', value=config_type), dict(name='@controller_id', value=controller_id)],
            enable_cross_partition_query=True)
        config_data = list(query_data)
        if len(config_data) == 1:
            return ControllerConfig(**config_data[0])
        return None
