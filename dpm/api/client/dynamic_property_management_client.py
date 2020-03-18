from typing import Dict, List
from cloudsecrets.gcp import Secrets

class DynamicPropertyManagementClient:
    def __init__(self,*args,**kwargs):
        self.service = kwargs.get('service',None)
        self.program = kwargs.get('program',None)
        self.polling_interval = kwargs.get('polling_interval', 0) 
        if not self.program or not self.service:
            raise Exception("Error: must provide service and program")
        self.secret_resource = f"dpm-{self.service}-{self.program}-config"
        self.properties = Secrets(self.secret_resource,polling_interval=self.polling_interval)
    def get_dynamic_properties(self) -> Dict[str, str]:
        return dict(self.properties)
