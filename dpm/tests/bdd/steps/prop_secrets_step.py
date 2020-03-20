from behave import *

from dpm.api.config.env_config import Env


@given("service_name is {service_name}")
def service_name(self, service_name):
    self.service_name = service_name


@step("program_name is {program_name}")
def program_name(self, program_name):
    self.program_name = program_name


@when("we read dict property {prop}")
def we_read_dict(self, prop):
    Env.initialize(self.service_name, self.program_name)
    self.result = Env.get_property_dict(prop)


@when("we read val property {prop}")
def we_read_val(self, prop):
    Env.initialize(self.service_name, self.program_name)
    self.result = Env.get_property_val(prop)


@then("we get dict {result}")
def we_get_dict(self, result):
    assert self.result["value"] == result


@then("we get val {result}")
def we_get_val(self, result):
    assert self.result == result


@given("test this")
def step_impl(context):
    while True:
        Env.initialize("data-integrations", "intacct", 5)
        result = Env.get_property_dict("destination")
        print(result)