# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time
from behave import *
from dpm.api.env import Env
from google.cloud import secretmanager
import json
from google.cloud import firestore

from dpm.tests.bdd.mocks.firestore_client_mock import FirestoreClientMock
from dpm.tests.bdd.mocks.secret_manager_service_client_mock import SecretManagerServiceClientMock

test_key: str = None
test_value: str = None


@given("mocks")
def mocks(context):
    secretmanager.SecretManagerServiceClient = SecretManagerServiceClientMock()
    firestore.Client = FirestoreClientMock()


@given("this exists {key} = {val}")
def key_and_value_exists(context, key, val):
    global test_key, test_value
    test_key = key
    test_value = val


@given("service_name is {service_name}")
def service_name(context, service_name):
    context.service_name = service_name


@step("program_name is {program_name}")
def program_name(context, program_name):
    context.program_name = program_name


@step("secrets_name {secrets_name}")
def secrets_name(context, secrets_name):
    context.secrets_name = secrets_name


@step("project is {project}")
def project(context, project):
    context.project = project


@step("dpm_polling_interval is {dpm_polling_interval}")
def dpm_polling_interval(context, dpm_polling_interval):
    context.dpm_polling_interval = dpm_polling_interval


@step("secrets_polling_interval is {secrets_polling_interval}")
def secrets_polling_interval(context, secrets_polling_interval):
    context.secrets_polling_interval = secrets_polling_interval


@when("we read property {prop}")
def we_read_property(context, prop):
    # global test_key, test_value
    Env.initialize(dpm_service_name=context.service_name, dpm_program_name=context.program_name,
                   secrets_name=context.secrets_name, secrets_polling_interval=int(context.secrets_polling_interval),
                   project=context.project)

    try:
        Env.dpm_client.properties = {test_key: json.loads(test_value)}
    except:
        Env.dpm_client.properties = {test_key: test_value}

    context.result = Env.get_property(prop)


@when("we read secret {secret}")
def we_read_secret(context, secret):
    Env.initialize(dpm_service_name=context.service_name, dpm_program_name=context.program_name,
                   secrets_name=context.secrets_name, secrets_polling_interval=int(context.secrets_polling_interval),
                   project=context.project)
    context.result = Env.get_secret(secret)


@then("we get val {result}")
def we_get_val(context, result):
    assert context.result == result


@given("test this")
def testing(context):
    counter = 0
    while True:
        property_value = Env.get_property("USD")
        secret_value = Env.get_secret("name")
        counter += 1
        print(f"{counter} : property={property_value} : secret={secret_value}")
        time.sleep(1)


@given("I start")
def start(context):
    # Env.initialize(dpm_service_name="data-integrations", dpm_program_name="intacct",
    #        secrets_name="data-integrations-secrets", secrets_polling_interval=10, project="dp2-stage")
    Env.initialize(dpm_service_name="data-integrations", dpm_program_name="intacct",
           secrets_name="data-integrations-secrets", secrets_polling_interval=10, project="imposing-union-227917")


@when("I update {key} = {value}")
def step_impl(context, key, value):
    Env.update_property(key, value)