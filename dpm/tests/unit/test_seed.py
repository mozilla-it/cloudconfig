import json
import unittest

import dpm.api.env as config
from dpm.api.seed import DynamicPropertiesSeeder
from dpm.tests.mocks import MockEnv


class DynamicPropertiesSeederTest(unittest.TestCase):

    def test_dynamic_property_seeder(context):
        config.Env = MockEnv()
        under_test = DynamicPropertiesSeeder(
            "prod", "dpm_service_name", "dpm/tests/resource/dynamic-properties-seed/", "partner_a"
        )
        under_test.execute()

        assert MockEnv.doc_data == json.loads(open("dpm/tests/resource/dynamic-properties-seed/prod/partner_a.json").read())
