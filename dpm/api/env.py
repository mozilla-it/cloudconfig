from dpm.api.clients import DynamicPropertyManagementClient, SecretsClient
import logging
import json


class Env:
    logger = logging.getLogger(__name__)
    dpm_service_name: str = None
    dpm_program_name: str = None
    secrets_name: str = None
    dpm_polling_interval: int = 0
    secrets_polling_interval: int = 0
    dpm_client: DynamicPropertyManagementClient = None
    secrets_client: SecretsClient = None
    initialized: bool = False

    @staticmethod
    def initialize(dpm_service_name: str, dpm_program_name: str, secrets_name: str, project: str,
                   dpm_polling_interval: int = 300, secrets_polling_interval: int = 0):

        Env.dpm_service_name = dpm_service_name
        Env.dpm_program_name = dpm_program_name
        Env.secrets_name = secrets_name
        Env.dpm_polling_interval = dpm_polling_interval
        Env.dpm_client = DynamicPropertyManagementClient(
            service_name=dpm_service_name, program_name=dpm_program_name, polling_interval=dpm_polling_interval, project=project)
        Env.secrets_client = SecretsClient(secrets_name=secrets_name, polling_interval=secrets_polling_interval, project=project)
        Env.initialized = True
        Env.logger.info(f"Initializing with dpm_service_name={dpm_service_name}, "
                        f"dpm_program_name={dpm_program_name}, "
                        f"secrets_name={secrets_name}, project={project}, "
                        f"dpm_polling_interval={dpm_polling_interval}, "
                        f"secrets_polling_interval={secrets_polling_interval}")

    @staticmethod
    def get_property(key: str) -> str:
        if Env.initialized is False:
            Env.logger.error("Trying to get_property without initialization")
            raise Exception("You must invoke Env.initialize with the appropriate parameters")

        try:
            return json.loads(Env.dpm_client.get_dynamic_properties().get(key)).get("value")
        except:
            return Env.dpm_client.get_dynamic_properties().get(key)

    @staticmethod
    def get_secret(key: str) -> str:
        if Env.initialized is False:
            Env.logger.error("Trying to get_secret without initialization")
            raise Exception("You must invoke Env.initialize with the appropriate parameters")
        return Env.secrets_client.get_secret(key)
