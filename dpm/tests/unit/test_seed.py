import pytest
import json


def test_dynamic_property_seeder(monkeypatch):
    import dpm.api.seed
    from dpm.api.seed import DynamicPropertiesSeeder

    test_props = {}

    def mock_initialize(*args, **kwargs):
        return None

    def mock_insert(*args, **kwargs):
        # global test_props
        test_props[args[0]] = args[1]

    monkeypatch.setattr(dpm.api.seed.Env, "initialize", mock_initialize)
    monkeypatch.setattr(dpm.api.seed.Env, "insert_property", mock_insert)

    seeder = DynamicPropertiesSeeder(
        "prod", "dpm_service_name", "dpm/tests/resource/dynamic-properties-seed/", "partner_a")
    seeder.execute()
    # print(test_props)
    assert test_props == json.loads(
        open("dpm/tests/resource/dynamic-properties-seed/prod/partner_a.json").read()
    )
