# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from behave import *

from dpm.api.seed import DynamicPropertiesSeeder


@given("directory with seed data {path}")
def directory(self, path):
    self.path = path


@given("env {env}")
def env(self, env):
    self.env = env


@given("seeding service {service}")
def step_impl(self, service):
    self.service = service


@when("we run seeding")
def run(self):
    seeder = DynamicPropertiesSeeder(self.env, self.service, self.path)
    seeder.execute()