from typing import Dict, List
from dpm.api.client.dynamic_property_management_client import DynamicPropertyManagementClient
from cloudsecrets.gcp import Secrets
import json
import logging


class Env:
    def __init__(self, env_id: int, service_id: int, secret_name: str, secret_keys: List[str], project: str):
        self.logger = logging.getLogger(__name__)
        _secrets = dict(Secrets(secret_name, project=project))
        self.local_properties: Dict[str, str] = \
            DynamicPropertyManagementClient().get_dynamic_properties(env_id=env_id, service_id=service_id)

        for k in secret_keys:
            assert k in _secrets.keys(), "Could not find key {}".format(k)
            loads = json.loads(_secrets[k])
            overlapping_keys = (self.local_properties.keys() & loads.keys())

            if len(overlapping_keys) > 0:
                self.logger.warning("OVERRIDING FIELDS {}".format(overlapping_keys))

            self.local_properties.update(loads)

    def get_property(self, key: str) -> str:
        return self.local_properties[key]

