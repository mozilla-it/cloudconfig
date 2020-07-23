from behave import *

from dpm.api.seed import DynamicPropertiesSeeder
from dpm.tests.bdd.steps.properties_secrets_step import DocumentMock


@given("directory with seed data {path}")
def directory(self, path):
    self.path = path


@given("we initialize the seeder")
def run(self):
    assert DocumentMock.properties is None
    self.seeder = DynamicPropertiesSeeder(self.service_name, self.path, self.program_name)
    assert DocumentMock.properties == dict()


@when("we run seeding")
def run(self):
    self.seeder.execute()
    assert DocumentMock.properties['MDC - 2'] == "hello"

