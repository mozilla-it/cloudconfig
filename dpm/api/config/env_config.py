from typing import Dict, List
from dpm.api.client.dynamic_property_management_client import DynamicPropertyManagementClient
from cloudsecrets.gcp import Secrets
import logging
import polling2
import os
import threading


class Env:
    local_properties: Dict[str, str] = None
    logger = logging.getLogger(__name__)
    env_id: int = None
    service_id: int = None
    program_id: int = None
    secret_name: str = None
    project: str = None
    is_initialized: bool = False
    client: DynamicPropertyManagementClient = None

    @staticmethod
    def initialize(env_id: int, service_id: int, program_id: int, secret_name: str, project: str):
        Env.env_id = env_id
        Env.service_id = service_id
        Env.program_id = program_id
        Env.secret_name = secret_name
        Env.project = project
        Env.is_initialized = True
        Env.client = DynamicPropertyManagementClient()
        Env._start()

    @staticmethod
    def _start_background_polling():
        d = threading.Thread(name='daemon', target=Polling.start)
        d.setDaemon(True)
        d.start()

    @staticmethod
    def get_property(key: str) -> str:
        if Env.is_initialized is False:
            raise Exception("Env has not been initialized. Please invoke Env.initialize before continuing.")
        return Env.local_properties[key]

    @staticmethod
    def _start():
        if Env.is_initialized:
            Env.local_properties = Env.build_properties()
            Env._start_background_polling()

    @staticmethod
    def build_properties():
        _secrets = dict(Secrets(Env.secret_name, project=Env.project))
        result: Dict[str, str] = Env.client.get_dynamic_properties(env_id=Env.env_id, service_id=Env.service_id, program_id=Env.program_id)
        overlapping_keys = (result.keys() & _secrets.keys())

        if len(overlapping_keys) > 0:
            Env.logger.warning("OVERRIDING FIELDS {}".format(overlapping_keys))

        result.update(_secrets)
        return result


class Polling:
    @staticmethod
    def start():
        polling2.poll(
            lambda: Polling.call_refresh(),
            step=int(os.getenv("DYNAMIC_PROPERTIES_PULL_DELAY")),
            poll_forever=True)

    @staticmethod
    def call_refresh():
        try:
            properties = Env.build_properties()
            if properties is not None:
                Env.local_properties = properties
        except Exception as e:
            Env.logger.warning("Could not build properties {}".format(e.args[0]))