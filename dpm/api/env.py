from typing import Dict

import dpm.api.clients
import logging


class Env:
    class InnerEnv:
        _dpm_instance: dpm.api.clients.DynamicPropertyManagementClient = None
        _secret_instance: dpm.api.clients.SecretsClient = None

        def __init__(self, dpm_service_name: str = None, dpm_program_name: str = None, secrets_name: str = None,
                     project: str = None,
                     secrets_polling_interval: int = 0):
            if Env.InnerEnv._dpm_instance is None:
                Env.InnerEnv._dpm_instance = dpm.api.clients.DynamicPropertyManagementClient(
                    service_name=dpm_service_name,
                    program_name=dpm_program_name)
            if Env.InnerEnv._secret_instance is None and (secrets_name is not None and project is not None):
                Env.InnerEnv._secret_instance = dpm.api.clients.SecretsClient(secrets_name=secrets_name,
                                                                              polling_interval=secrets_polling_interval,
                                                                              project=project)

        def get_property(self, key: str):
            keys = self._dpm_instance.get_dynamic_properties().keys()

            if key in keys:
                property_val = self._dpm_instance.get_dynamic_properties().get(key)
                if isinstance(property_val, Dict):
                    dict_keys = property_val.keys()
                    if "value" in dict_keys:
                        return property_val.get("value")

                    return property_val

                return property_val

            raise Exception(f"{key} not found!")

        def update_property(self, key: str, value):
            self._dpm_instance.update_property(key=key, value=value)

        def insert_property(self, key: str, value):
            self._dpm_instance.insert_property(key=key, value=value)

        def get_secret(self, key: str) -> str:
            return self._secret_instance.get_secret(key)

    _instance: InnerEnv = None

    def __init__(self, dpm_service_name: str = None, dpm_program_name: str = None, secrets_name: str = None,
                 project: str = None,
                 secrets_polling_interval: int = 0):
        if not Env._instance:
            Env._instance = Env.InnerEnv(dpm_service_name=dpm_service_name, dpm_program_name=dpm_program_name,
                                         secrets_name=secrets_name, project=project,
                                         secrets_polling_interval=secrets_polling_interval)

    def get_instance(self):
        return self._instance
