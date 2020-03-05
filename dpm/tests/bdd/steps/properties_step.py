import time
from datetime import datetime
from unittest.mock import MagicMock, Mock
import os
import json
from google.cloud import bigquery
os.environ["DYNAMIC_PROPERTIES_URL"] = "http://127.0.0.1:8000"
from behave import *
import requests
import cloudsecrets.gcp
cloudsecrets.gcp.Secrets = Mock(return_value={"box.json": '{\n  "boxAppSettings": {\n    "clientID": "mockedclientid",\n    "clientSecret": "mockedclientSecret"}}'})
from dpm.api.config.env_config import Env
env_id = None
service_id = None
program_id = None
property_value = None
secret_name = None


class PropertyResponseMock(MagicMock):
    status_code = 200
    text = """[{"env_id":224,"value":"0","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"Revenue inserts happen in batch format for all partners. This number tells the system how long to pause between inserts. This should be leverage if the destination is under stress. We are not expecting this since we are working with BigQuery.","key":"REVENUE_SLEEP_TIME_BETWEEN_INSERTS","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"imposing-union-227917.revenue.revenue_data","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"This is the destination table in BigQuery. It should be structured like: <projectId/>.<dataset/>.<tableName/>","key":"REVENUE_DATA_DESTINATION","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"imposing-union-227917","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"The project id in GCP for this environment.","key":"PROJECT_ID","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"False","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"This configuration is used to tell the system to read from a specific path. If this is set to True when we process the path we are assuming a structure like: <year/>/folder/another-folder. If this is set to False then the system will append the current year to the name of the folder passed in. Look at PARTNET_MAPS* and how the relate to the folders in play at any given time.","key":"REVENUE_FORCE_BOX_PATH","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"0.895","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"This is the Bind default value we use to perform Bing calculations. It is provided by the customer. Reach out to arana@mozilla.com for more information on this number.","key":"BING_DEFAULT_GROSS_REVENUE_DENOMINATOR","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"2019","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"If REVENUE_FORCE_BOX_PATH is not set, then we assume a single folder and we append the current year to the front of the path. If we want to override the year and force the system to process a specific year we should set this field. Else this field should not be set.","key":"FORCED_YEAR","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"Bing","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"This maps the folder the partner uses in box.com vs the name we internally use to identify the partner. In this case Bing == Bing","key":"PARTNER_MAPS_BING","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"Google US & International/Automation","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"This maps the folder the partner uses in box.com vs the name we internally use to identify the partner. In this case GoogleRevenue == Google US & International/Automation","key":"PARTNER_MAPS_GOOGLEREVENUE","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"Yandex","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"This maps the folder the partner uses in box.com vs the name we internally use to identify the partner. In this case Yandex == Yandex","key":"PARTNER_MAPS_YANDEX","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"1000","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"The inserts into BigQuery happen if batch format. This number tells the system how many records to batch before performing the insert. This is a consistent number for all partners.","key":"REVENUE_BUFFER_BEFORE_INSERT","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"},{"env_id":224,"value":"9864028249","program_id":788,"created_date":"2020-03-04T13:56:08.456154","description":"This is the box user id the application uses to login and retrieve data. Note: if this account lacks the necessary permissions the software will not be able to complete its task.","key":"BOX_USER_ID","service_id":568,"updated_date":"2020-03-04T13:56:08.456154"}]"""


class TokenResponseMock(MagicMock):
    status_code = 200
    text = """{"access_token": "PIUHHIUIHJKHKHIIUYKUHHJKH"}"""


class DictMock(MagicMock):
    def __init__(self, **kwargs):
        pass


@given("mocks")
def mocks(context):
    bigquery.Client = MagicMock()
    m = Mock()
    m.side_effect = [TokenResponseMock(), PropertyResponseMock()]
    requests.post = m


@given("the env id is {p_env_id}")
def env_id(context, p_env_id):
    context.env_id = p_env_id


@step("the service id is {p_service_id}")
def service_id(context, p_service_id):
    context.service_id = p_service_id


@when("we call {prop_name}")
def we_call(context, prop_name):
    context.property_value = Env.get_property(prop_name)


@then("we receive {val}")
def we_receive(context, val):
    assert context.property_value == val


@then("dict we receive {val}")
def dict_we_receive(context, val):
    assert context.property_value == json.loads(val)


@step("secret_name {p_secret_name}")
def secret_name(context, p_secret_name):
    context.secret_name = p_secret_name


@step("project is {p_project}")
def project_is(context, p_project):
    context.project = p_project


@step("I initialize the system")
def initialize(context):
    Env.initialize(env_id=context.env_id, service_id=context.service_id, program_id=context.program_id,
              secret_name=context.secret_name, project=context.project)


@given("keep running")
def step_impl(context):
    while True:
        result = Env.get_property("BOX_USER_ID")
        print(result, datetime.now())
        time.sleep(1)


@step("the program id is {p_program_id}")
def step_impl(context, p_program_id):
    context.program_id = p_program_id