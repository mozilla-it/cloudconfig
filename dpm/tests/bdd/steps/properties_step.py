from google.cloud import bigquery
from unittest.mock import MagicMock, Mock
import os
import json
os.environ["DYNAMIC_PROPERTIES_URL"] = "someurl"
from behave import *
import requests
import cloudsecrets.gcp
cloudsecrets.gcp.Secrets = Mock(return_value={"box.json": '{\n  "boxAppSettings": {\n    "clientID": "mockedclientid",\n    "clientSecret": "mockedclientSecret"}}'})
from dpm.api.config.env_config import Env
env_id = None
service_id = None
property_value = None
secret_name = None


class ResponseMock(MagicMock):
    text = "[{\"env_id\":224,\"key\":\"REVENUE_SLEEP_TIME_BETWEEN_INSERTS\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"0\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"REVENUE_DATA_DESTINATION\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"imposing-union-227917.revenue.revenue_data\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"PROJECT_ID\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"imposing-union-227917\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"REVENUE_FORCE_BOX_PATH\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"False\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"FORCED_YEAR\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"2019\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"PARTNER_MAPS_BING\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"Bing\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"PARTNER_MAPS_GOOGLEREVENUE\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"Google US & International/Automation\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"PARTNER_MAPS_YANDEX\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"Yandex\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"REVENUE_BUFFER_BEFORE_INSERT\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"1000\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"BOX_USER_ID\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"9864028249\",\"updated_date\":\"2020-02-19T19:25:37.183236\"},{\"env_id\":224,\"key\":\"BING_DEFAULT_GROSS_REVENUE_DENOMINATOR\",\"created_date\":\"2020-02-19T19:25:37.183236\",\"service_id\":568,\"value\":\"0.895\",\"updated_date\":\"2020-02-19T19:25:37.183236\"}]"


class DictMock(MagicMock):
    def __init__(self, **kwargs):
        pass


@given("mocks")
def mocks(context):
    bigquery.Client = MagicMock()
    requests.post = ResponseMock()


@given("the env id is {p_env_id}")
def env_id(context, p_env_id):
    context.env_id = p_env_id


@step("the service id is {p_service_id}")
def service_id(context, p_service_id):
    context.service_id = p_service_id


@when("we call {prop_name}")
def we_call(context, prop_name):
    env = Env(env_id=context.env_id, service_id=context.service_id,
              secret_name=context.secret_name, secret_keys=context.secret_keys, project=context.project)
    context.property_value = env.get_property(prop_name)


@then("we receive {val}")
def we_receive(context, val):
    assert context.property_value == val


@then("dict we receive {val}")
def dict_we_receive(context, val):
    assert context.property_value == json.loads(val)


@step("secret_name {p_secret_name}")
def secret_name(context, p_secret_name):
    context.secret_name = p_secret_name


@step("secret_keys")
def secret_keys(context):
    table = context.table
    context.secret_keys = list()
    for r in table:
        context.secret_keys.append(r["key"])


@step("project is {p_project}")
def project_is(context, p_project):
    context.project = p_project
