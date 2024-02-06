import uuid


class ControllerConfig:
    # def __init__(self, controller_id, topic_name, config_name, config_des, subscription, authorization_key):
    #     self.id = uuid.uuid4()
    #     self.controller_id = controller_id
    #     self.topic_name = topic_name
    #     self.config_name = config_name
    #     self.config_des = config_des
    #     self.subscription = subscription
    #     self.authorization_key = authorization_key
    def __init__(self, **entries):
        self.__dict__.update(entries)
