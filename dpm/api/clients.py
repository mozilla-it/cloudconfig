from typing import Dict
import cloudsecrets.gcp
from google.cloud import firestore


class DynamicPropertyManagementClient:
    properties: Dict[str, str] = dict()

    def __init__(self, service_name: str, program_name: str):
        def on_snapshot(doc_snapshot, changes, read_time):
            for change in changes:
                self.properties = change.document.to_dict()

        self.service = service_name
        self.program = program_name
        if not self.program or not self.service:
            raise Exception("Error: must provide service name and program name")

        self.doc_path = f"dpm-configs/{self.service}-{self.program}"
        self.firestore_client = firestore.Client()
        self.doc_ref = self.firestore_client.document(self.doc_path)

        if self.doc_ref.get().exists is False:
            self.doc_ref.set({})

        self.properties = self.doc_ref.get().to_dict()
        doc_watch = self.doc_ref.on_snapshot(on_snapshot)

    def get_dynamic_properties(self) -> Dict[str, str]:
        if self.properties:
            return dict(self.properties)
        else:
            return dict()

    def update_property(self, key: str, value):
        doc = self.doc_ref.get().to_dict()
        doc.update({key: value})
        self.doc_ref.set(doc)

    def insert_property(self, key: str, value):
        doc = self.doc_ref.get().to_dict()
        if doc.get(key) is None:
            doc.update({key: value})

        self.doc_ref.set(doc)


class SecretsClient:
    def __init__(self, secrets_name: str, project: str, polling_interval: int = 0):
        self.secrets_name = secrets_name
        self.polling_interval = polling_interval
        if not self.secrets_name:
            raise Exception("Error: must have secret_name")
        self.secrets = cloudsecrets.gcp.Secrets(
            self.secrets_name, polling_interval=self.polling_interval, project=project
        )

    def get_secret(self, key: str) -> str:
        return dict(self.secrets).get(key)
