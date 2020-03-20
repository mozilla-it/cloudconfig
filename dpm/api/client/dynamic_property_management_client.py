from typing import Dict
from cloudsecrets.gcp import Secrets


class DynamicPropertyManagementClient:

    def __init__(self, service_name: str, program_name: str, polling_interval: int = 0):
        self.service = service_name
        self.program = program_name
        self.polling_interval = polling_interval
        if not self.program or not self.service:
            raise Exception("Error: must provide service name and program name")
        self.secret_resource = f"dpm-{self.service}-{self.program}-config"
        self.properties = Secrets(self.secret_resource,polling_interval=self.polling_interval)

    def get_dynamic_properties(self) -> Dict[str, str]:
        return dict(self.properties)
