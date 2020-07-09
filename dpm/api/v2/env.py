# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Dict

from dpm.api.clients import DynamicPropertyManagementClient, SecretsClient


class CloudConfigFascade:
    def __init__(self,
                 service_name,
                 program_name,
                 secrets_name,
                 project,
                 secrets_polling_interval=30):
        self.firestore_wrapper = DynamicPropertyManagementClient(service_name=service_name, program_name=program_name)
        self.secrets_wrapper = SecretsClient(secrets_name=secrets_name, polling_interval=secrets_polling_interval, project=project)

    def get_property(self, key: str):
        keys = self.firestore_wrapper.get_dynamic_properties().keys()
        if key in keys:
            property_val = self.firestore_wrapper.get_dynamic_properties().get(key)
            if isinstance(property_val, Dict):
                dict_keys = property_val.keys()
                if "value" in dict_keys:
                    return property_val.get("value")
                return property_val
            return property_val
        raise Exception(f"{key} not found!")

    def update_property(self, key: str, value):
        self.firestore_wrapper.update_property(key=key, value=value)

    def insert_property(self, key: str, value):
        self.firestore_wrapper.insert_property(key=key, value=value)

    def get_secret(self, key: str) -> str:
        return self.secrets_wrapper.get_secret(key)
