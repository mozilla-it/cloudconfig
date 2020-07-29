# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from typing import Dict

from . import clients


class Env:
    logger = logging.getLogger(__name__)
    dpm_service_name: str = None
    dpm_program_name: str = None
    secrets_name: str = None
    secrets_polling_interval: int = 0
    dpm_client: clients.DynamicPropertyManagementClient = None
    secrets_client: clients.SecretsClient = None
    dpm_initialized: bool = False
    secrets_initialized: bool = False

    def __init__(
        self,
        dpm_service_name: str,
        dpm_program_name: str,
        secrets_name: str = None,
        project: str = None,
        secrets_polling_interval: int = 0,
    ):
        # Setting up dynamic properties
        self.dpm_service_name = dpm_service_name
        self.dpm_program_name = dpm_program_name
        self.dpm_client = clients.DynamicPropertyManagementClient(
            service_name=dpm_service_name, program_name=dpm_program_name
        )
        self.dpm_initialized = True

        # Setting up secrets manager
        if secrets_name is not None and project is not None:
            self.secrets_name = secrets_name
            self.secrets_client = clients.SecretsClient(
                secrets_name=secrets_name,
                polling_interval=secrets_polling_interval,
                project=project,
            )
            self.secrets_initialized = True
            self.logger.info(
                f"Initializing with dpm_service_name={dpm_service_name}, "
                f"dpm_program_name={dpm_program_name}, "
                f"secrets_name={secrets_name}, project={project}, "
                f"secrets_polling_interval={secrets_polling_interval}"
            )

    def get_property(self, key: str):
        if self.dpm_initialized is False:
            self.logger.error("Trying to get_property without initialization")
            raise Exception(
                "You must invoke Env.initialize with the appropriate parameters"
            )

        keys = self.dpm_client.get_dynamic_properties().keys()
        if key in keys:
            property_val = self.dpm_client.get_dynamic_properties().get(key)
            if isinstance(property_val, Dict):
                dict_keys = property_val.keys()
                if "value" in dict_keys:
                    return property_val.get("value")

                return property_val

            return property_val

        raise Exception(f"{key} not found!")

    def update_property(self, key: str, value):
        if self.dpm_initialized is False:
            self.logger.error("Trying to update_property without initialization")
            raise Exception(
                "You must invoke initialize with the appropriate parameters"
            )

        self.dpm_client.update_property(key=key, value=value)

    def insert_property(self, key: str, value):
        if self.dpm_initialized is False:
            self.logger.error("Trying to insert_property without initialization")
            raise Exception(
                "You must invoke initialize with the appropriate parameters"
            )

        self.dpm_client.insert_property(key=key, value=value)

    def get_secret(self, key: str) -> str:
        if self.secrets_initialized is False:
            self.logger.error("Trying to get_secret without initialization")
            raise Exception(
                "You must invoke initialize with the appropriate parameters"
            )
        return self.secrets_client.get_secret(key)
