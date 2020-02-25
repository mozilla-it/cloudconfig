from typing import Dict, List
import requests
import json
import os


class DynamicPropertyManagementClient:
    URL = str(os.environ["DYNAMIC_PROPERTIES_URL"]) + "/get_properties"

    def get_dynamic_properties(self, env_id: int, service_id: int) -> Dict[str, str]:
        result: Dict[str, str] = dict()
        params = {"env_id": env_id, "service_id": service_id}
        response = requests.post(self.URL, data=json.dumps(params))
        loads: List = json.loads(response.text)
        for l in loads:
            result.update({l["key"]: l["value"]})

        return result
