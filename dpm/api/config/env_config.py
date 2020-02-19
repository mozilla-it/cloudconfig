from typing import Dict

from api.client.dynamic_property_management_client import DynamicPropertyManagementClient


class Env:
    def __init__(self, env: str, service_id: str):
        self.local_properties: Dict[str, str] = DynamicPropertyManagementClient().get_dynamic_properties(env, service_id)
        self.env = env
        self.service_id = service_id

    def get_property(self, key: str):
        return self.local_properties[key]

    def update_property(self, key: str, value: str):
        self.local_properties.update({key: value})

