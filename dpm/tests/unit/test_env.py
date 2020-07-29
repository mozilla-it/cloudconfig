import pytest
from unittest import mock


def test_Env(monkeypatch):
    import dpm.api.env
    from dpm.api.env import Env

    def mock_clients(*args, **kwargs):
        mock_client = mock.MagicMock()
        mock_client.get_dynamic_properties.return_value = {
            "fake_key": {"prop_hash": "fake_value"}
        }
        return mock_client

    monkeypatch.setattr(
        dpm.api.env.clients, "DynamicPropertyManagementClient", mock_clients
    )
    monkeypatch.setattr(dpm.api.env.clients, "SecretsClient", mock_clients)
    environment = Env("something", "something")
    assert environment != None
    assert environment.dpm_initialized
    assert not environment.secrets_initialized

    # uninitialized call to get_property throws exception
    environment.dpm_initialized = False
    with pytest.raises(Exception):
        assert environment.get_property("something")

    # initialized call to get_property but with absent key throws exception
    environment.dpm_initialized = True
    with pytest.raises(Exception):
        assert environment.get_property("something")

    # initialized call to get_property but with key is fine
    environment.dpm_initialized = True
    assert environment.get_property("fake_key") == {"prop_hash": "fake_value"}

    # uninitialized call to update_property throws exception
    environment.dpm_initialized = False
    with pytest.raises(Exception):
        assert environment.update_property("key", "value")

    # initialized call to update_property is fine
    environment.dpm_initialized = True
    assert environment.update_property("key", "value") == None

    # uninitialized call to insert_property throws exception
    environment.dpm_initialized = False
    with pytest.raises(Exception):
        assert environment.insert_property("key", "value")

    # initialized call to insert_property is fine
    environment.dpm_initialized = True
    assert environment.insert_property("key", "value") == None

    # uninitialized call to get_secret throws exception
    environment.secrets_initialized = False
    with pytest.raises(Exception):
        assert environment.get_secret("key")
