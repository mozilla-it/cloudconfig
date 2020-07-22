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

    assert Env.initialize("something", "something") == None
    assert Env.dpm_initialized
    assert not Env.secrets_initialized

    # uninitialized call to get_property throws exception
    Env.dpm_initialized = False
    with pytest.raises(Exception):
        assert Env.get_property("something")

    # initialized call to get_property but with absent key throws exception
    Env.dpm_initialized = True
    with pytest.raises(Exception):
        assert Env.get_property("something")

    # initialized call to get_property but with key is fine
    Env.dpm_initialized = True
    assert Env.get_property("fake_key") == {"prop_hash": "fake_value"}

    # uninitialized call to update_property throws exception
    Env.dpm_initialized = False
    with pytest.raises(Exception):
        assert Env.update_property("key", "value")

    # initialized call to update_property is fine
    Env.dpm_initialized = True
    assert Env.update_property("key", "value") == None

    # uninitialized call to insert_property throws exception
    Env.dpm_initialized = False
    with pytest.raises(Exception):
        assert Env.insert_property("key", "value")

    # initialized call to insert_property is fine
    Env.dpm_initialized = True
    assert Env.insert_property("key", "value") == None

    # uninitialized call to get_secret throws exception
    Env.secrets_initialized = False
    with pytest.raises(Exception):
        assert Env.get_secret("key")
