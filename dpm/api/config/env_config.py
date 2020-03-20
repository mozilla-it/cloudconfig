from typing import Dict
from dpm.api.client.dynamic_property_management_client import DynamicPropertyManagementClient
import logging
import json


class Env:
    logger = logging.getLogger(__name__)
    service_name: str = None
    program_name: str = None
    polling_interval: int = 0
    client: DynamicPropertyManagementClient = None

    @staticmethod
    def initialize(service_name: str, program_name: str, polling_interval: int = 300):
        Env.service_name = service_name
        Env.program_name = program_name
        Env.polling_interval = polling_interval
        Env.client = DynamicPropertyManagementClient(service_name=service_name, program_name=program_name, polling_interval=polling_interval)

    @staticmethod
    def get_property_dict(key: str) -> Dict[str, str]:
        return json.loads(Env.client.get_dynamic_properties().get(key))

    @staticmethod
    def get_property_val(key: str) -> str:
        return json.loads(Env.client.get_dynamic_properties().get(key)).get("value", None)
