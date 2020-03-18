from typing import Dict, List
from dpm.api.client.dynamic_property_management_client import DynamicPropertyManagementClient
from cloudsecrets.gcp import Secrets
import logging
import json


class Env:
    local_properties: Dict[str, str] = None
    logger = logging.getLogger(__name__)
    service: str = None
    program: str = None
    secret_name: str = None
    is_initialized: bool = False
    polling_interval: int = 0
    client: DynamicPropertyManagementClient = None

    @staticmethod
    def initialize(service: str, program: str, polling_interval: int = 300):
        Env.service = service
        Env.program = program
        Env.polling_interval = polling_interval
        Env.is_initialized = True
        Env.client = DynamicPropertyManagementClient(service=service,program=program,polling_interval=polling_interval)
        Env._start()

    @staticmethod
    def _start_background_polling():
        d = threading.Thread(name='daemon', target=Polling.start)
        d.setDaemon(True)
        d.start()

    @staticmethod
    def get_property(key: str) -> str:
        if not Env.is_initialized:
            raise Exception("Env has not been initialized. Please invoke Env.initialize before continuing.")
        Env.local_properties = Env.build_properties()
        return json.loads(Env.local_properties[key]).get("value","")

    @staticmethod
    def _start():
        if Env.is_initialized:
            Env.local_properties = Env.build_properties()

    @staticmethod
    def build_properties():
        result: Dict[str, str] = Env.client.get_dynamic_properties()
        return result
