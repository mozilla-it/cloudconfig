from typing import Dict, List
import requests
import json
import os
from retry import retry


class DynamicPropertyManagementClient:
    URL = str(os.getenv("DYNAMIC_PROPERTIES_URL")) + "/get_properties"
    URL_TOKEN = str(os.getenv("DYNAMIC_PROPERTIES_URL")) + "/token"
    TOKEN = None

    def get_dynamic_properties(self, env_id: int, service_id: int, program_id: int) -> Dict[str, str]:
        if env_id is None or service_id is None:
            return dict()

        if self.TOKEN is None:
            self.TOKEN = self.get_token()

        result: Dict[str, str] = dict()
        params = {"env_id": env_id, "service_id": service_id, "program_id": program_id}
        response = self._post_for_properties(params)

        loads: List = json.loads(response.text)
        for l in loads:
            result.update({l["key"]: l["value"]})

        return result

    @retry(ValueError, tries=3)
    def _post_for_properties(self, params):
        head = {'Authorization': 'Bearer ' + self.TOKEN}
        response = requests.post(self.URL, data=json.dumps(params), headers=head)
        if response.status_code not in [200, 201]:
            self.TOKEN = self.get_token()
            raise ValueError(response.text)

        return response

    def get_token(self) -> str:
        data = {"username": os.getenv("USERNAME"), "password": os.getenv("PASSWORD")}
        response = requests.post(self.URL_TOKEN, data=data)
        return json.loads(response.text)["access_token"]