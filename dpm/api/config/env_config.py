from typing import Dict, List
from dpm.api.client.dynamic_property_management_client import DynamicPropertyManagementClient
from cloudsecrets.gcp import Secrets
import json
import logging
import polling2
import os
import threading


class Env:
    local_properties = None
    logger = None
    env_id = None
    service_id = None
    secret_name = None
    secret_keys = None
    project = None
    is_initialized = False
    client = None

    @staticmethod
    def initialize(env_id: int, service_id: int, secret_name: str, secret_keys: List[str], project: str):
        Env.logger = logging.getLogger(__name__)
        Env.env_id: int = env_id
        Env.service_id: int = service_id
        Env.secret_name: str = secret_name
        Env.secret_keys: List[str] = secret_keys
        Env.project: str = project
        Env.is_initialized = True
        Env.client = DynamicPropertyManagementClient()
        Env._start()
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
            Env.local_properties: Dict[str, str] = Env.build_properties()

    @staticmethod
    def build_properties():
        _secrets = dict(Secrets(Env.secret_name, project=Env.project))
        result: Dict[str, str] = \
            Env.client.get_dynamic_properties(env_id=Env.env_id, service_id=Env.service_id)

        for k in Env.secret_keys:
            assert k in _secrets.keys(), "Could not find key {}".format(k)
            loads = json.loads(_secrets[k])
            overlapping_keys = (result.keys() & loads.keys())

            if len(overlapping_keys) > 0:
                Env.logger.warning("OVERRIDING FIELDS {}".format(overlapping_keys))

            result.update(loads)

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
        properties = Env.build_properties()
        if properties is not None:
            Env.local_properties = properties
