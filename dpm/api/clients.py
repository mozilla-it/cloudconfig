from typing import Dict
from cloudsecrets.gcp import Secrets
from google.cloud import firestore


class DynamicPropertyManagementClient:

    def __init__(self, service_name: str, program_name: str, project: str, polling_interval: int = 0):
        def on_snapshot(doc_snapshot, changes, read_time):
            for change in changes:
                self.properties = change.document.to_dict()

        self.service = service_name
        self.program = program_name
        self.polling_interval = polling_interval
        if not self.program or not self.service:
            raise Exception("Error: must provide service name and program name")
        self.doc_path = f"dpm-configs/{self.service}-{self.program}"
        self.firestore_client = firestore.Client()
        self.doc_ref = self.firestore_client.document(self.doc_path)
        doc_watch = self.doc_ref.on_snapshot(on_snapshot)

    def get_dynamic_properties(self) -> Dict[str, str]:
        return dict(self.properties)


class SecretsClient:

    def __init__(self, secrets_name: str, project: str, polling_interval: int = 0):
        self.secrets_name = secrets_name
        self.polling_interval = polling_interval
        if not self.secrets_name:
            raise Exception("Error: must secret_name")
        self.secrets = Secrets(self.secrets_name, polling_interval=self.polling_interval, project=project)

    def get_secret(self, key: str) -> str:
        return dict(self.secrets).get(key)
