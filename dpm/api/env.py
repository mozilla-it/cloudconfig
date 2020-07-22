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

    @staticmethod
    def initialize(dpm_service_name: str, dpm_program_name: str, secrets_name: str = None, project: str = None,
                   secrets_polling_interval: int = 0):

        # Setting up dynamic properties
        Env.dpm_service_name = dpm_service_name
        Env.dpm_program_name = dpm_program_name
        Env.dpm_client = clients.DynamicPropertyManagementClient(
            service_name=dpm_service_name, program_name=dpm_program_name)
        Env.dpm_initialized = True

        # Setting up secrets manager
        if secrets_name is not None and project is not None:
            Env.secrets_name = secrets_name
            Env.secrets_client = clients.SecretsClient(secrets_name=secrets_name,
                                                       polling_interval=secrets_polling_interval, project=project)
            Env.secrets_initialized = True
            Env.logger.info(f"Initializing with dpm_service_name={dpm_service_name}, "
                            f"dpm_program_name={dpm_program_name}, "
                            f"secrets_name={secrets_name}, project={project}, "
                            f"secrets_polling_interval={secrets_polling_interval}")

    @staticmethod
    def get_property(key: str):
        if Env.dpm_initialized is False:
            Env.logger.error("Trying to get_property without initialization")
            raise Exception("You must invoke Env.initialize with the appropriate parameters")

        keys = Env.dpm_client.get_dynamic_properties().keys()

        if key in keys:
            property_val = Env.dpm_client.get_dynamic_properties().get(key)
            if isinstance(property_val, Dict):
                dict_keys = property_val.keys()
                if "value" in dict_keys:
                    return property_val.get("value")

                return property_val

            return property_val

        raise Exception(f"{key} not found!")

    @staticmethod
    def update_property(key: str, value):
        if Env.dpm_initialized is False:
            Env.logger.error("Trying to update_property without initialization")
            raise Exception("You must invoke Env.initialize with the appropriate parameters")

        Env.dpm_client.update_property(key=key, value=value)

    @staticmethod
    def insert_property(key: str, value):
        if Env.dpm_initialized is False:
            Env.logger.error("Trying to insert_property without initialization")
            raise Exception("You must invoke Env.initialize with the appropriate parameters")

        Env.dpm_client.insert_property(key=key, value=value)

    @staticmethod
    def get_secret(key: str) -> str:
        if Env.secrets_initialized is False:
            Env.logger.error("Trying to get_secret without initialization")
            raise Exception("You must invoke Env.initialize with the appropriate parameters")
        return Env.secrets_client.get_secret(key)
