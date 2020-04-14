import time
from typing import List
from unittest.mock import Mock
import base64
from behave import *
from dpm.api.env import Env
from google.cloud import secretmanager
import json
from google.cloud import firestore

test_key: str = None
test_value: str = None


class MockObj(List):
    pass


class MockData:
    def __init__(self):
        global test_key, test_value
        val = base64.b64encode(test_value.encode('ascii'))
        vdict = {test_key: val.decode()}
        val1 = json.dumps(vdict)
        self.data = val1.encode("utf-8")


class MockX:
    def __init__(self):
        self.name = "one/1"
        self.payload = MockData()


class SecretManagerServiceClientMock(Mock):
    def list_secret_versions(self, x):
        return list(list(MockObj()))

    def secret_path(self, x, y):
        return Mock()

    def list_secret_versions(self, x):
        return [MockX()]

    def access_secret_version(self, p):
        return MockX()


class DocumentMock(Mock):
    def on_snapshot(self, v):
        return Mock()


class FirestoreClientMock(Mock):
    def document(self, v):
        return DocumentMock()


@given("mocks")
def mocks(context):
    secretmanager.SecretManagerServiceClient = SecretManagerServiceClientMock()
    firestore.Client = FirestoreClientMock()


@given("this exists {key} = {val}")
def step_impl(context, key, val):
    global test_key, test_value
    test_key = key
    test_value = val


@given("service_name is {service_name}")
def service_name(self, service_name):
    self.service_name = service_name


@step("program_name is {program_name}")
def program_name(self, program_name):
    self.program_name = program_name


@step("secrets_name {secrets_name}")
def secrets_name(self, secrets_name):
    self.secrets_name = secrets_name


@step("project is {project}")
def project(self, project):
    self.project = project


@step("dpm_polling_interval is {dpm_polling_interval}")
def dpm_polling_interval(self, dpm_polling_interval):
    self.dpm_polling_interval = dpm_polling_interval


@step("secrets_polling_interval is {secrets_polling_interval}")
def secrets_polling_interval(self, secrets_polling_interval):
    self.secrets_polling_interval = secrets_polling_interval


@when("we read property {prop}")
def we_read_property(self, prop):
    global test_key, test_value
    Env.initialize(dpm_service_name=self.service_name, dpm_program_name=self.program_name,
                   secrets_name=self.secrets_name, secrets_polling_interval=int(self.secrets_polling_interval),
                   project=self.project)

    try:
        Env.dpm_client.properties = {test_key: json.loads(test_value)}
    except:
        Env.dpm_client.properties = {test_key: test_value}

    self.result = Env.get_property(prop)


@when("we read secret {secret}")
def we_read_secret(self, secret):
    Env.initialize(dpm_service_name=self.service_name, dpm_program_name=self.program_name,
                   secrets_name=self.secrets_name, secrets_polling_interval=int(self.secrets_polling_interval),
                   project=self.project)
    self.result = Env.get_secret(secret)


@then("we get val {result}")
def we_get_val(self, result):
    assert self.result == result


@given("test this poll properties {prop_poll} and poll secrets {secrets_poll}")
def testing(context, prop_poll, secrets_poll):
    Env.initialize(dpm_service_name="data-integrations", dpm_program_name="intacct",
                   secrets_name="data-integrations-secrets", secrets_polling_interval=int(secrets_poll), project="imposing-union-227917")
    counter = 0
    while True:
        property_value = Env.get_property("USD")
        secret_value = Env.get_secret("name")
        counter += 1
        print(f"{counter} : property={property_value} : secret={secret_value}")
        time.sleep(1)

