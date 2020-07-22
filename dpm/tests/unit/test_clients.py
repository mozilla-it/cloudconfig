import mockfirestore
import pytest
from mockfirestore import MockFirestore
from mockfirestore._helpers import (
    generate_random_string,
    get_by_path,
    set_by_path,
)


class MyMockFirestore(MockFirestore):
    def __init__(self):
        super().__init__()

    class MyCollectionReference(mockfirestore.collection.CollectionReference):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def document(self, name=None):
            collection = get_by_path(self._data, self._path)
            if name is None:
                name = generate_random_string()
            new_path = self._path + [name]
            if name not in collection:
                set_by_path(self._data, new_path, {})
            return MyMockFirestore.MyDocumentReference(
                self._data, new_path, parent=self
            )

    class MyDocumentReference(mockfirestore.document.DocumentReference):
        class FakeSnapshot:
            def document(self):
                pass

            document.to_dict = lambda: {}  # type: ignore

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def on_snapshot(self, *args, **kwargs):
            args[0]("nothing", [self.FakeSnapshot()], "nothing")
            return None

    def collection(self, name):
        if name not in self._data:
            self._data[name] = {}
        return MyMockFirestore.MyCollectionReference(self._data, [name])

    def document(self, path):
        path_list = path.split("/", 2)
        return self.collection(path_list[0]).document(path_list[1])


def test_dynamic_property_mgmt_client(monkeypatch):
    import dpm.api.clients
    from dpm.api.clients import DynamicPropertyManagementClient

    def mock_initialize(*args, **kwargs):
        return MyMockFirestore()

    monkeypatch.setattr(dpm.api.clients.firestore, "Client", mock_initialize)

    with pytest.raises(Exception):
        assert DynamicPropertyManagementClient(None, None)

    client = DynamicPropertyManagementClient("dpm_service_name", "program_name")
    assert isinstance(client, dpm.api.clients.DynamicPropertyManagementClient)

    client.properties = None
    result = client.get_dynamic_properties()
    assert result == dict()

    client = DynamicPropertyManagementClient("dpm_service_name", "program_name")
    assert isinstance(client, dpm.api.clients.DynamicPropertyManagementClient)

    client.update_property("pickles", "pickles_value")
    # fake the reloading of properties "on_snapshot"
    # b/c MockFirestore doesn't implement that:
    client.properties = client.doc_ref.get().to_dict()
    assert client.get_dynamic_properties()["pickles"] == "pickles_value"

    client.insert_property("pickles", "new_pickles_value")
    # fake the reloading of properties "on_snapshot"
    # b/c MockFirestore doesn't implement that:
    client.properties = client.doc_ref.get().to_dict()
    # shouldn't change b/c insert_property won't overwrite
    assert client.get_dynamic_properties()["pickles"] == "pickles_value"

    client.insert_property("new_key", "new_value")
    # fake the reloading of properties "on_snapshot"
    # b/c MockFirestore doesn't implement that:
    client.properties = client.doc_ref.get().to_dict()
    assert client.get_dynamic_properties()["new_key"] == "new_value"

    from dpm.api.clients import SecretsClient

    with pytest.raises(Exception):
        assert SecretsClient(None, "project")
        assert SecretsClient()
        assert SecretsClient("", "project")
        assert SecretsClient(0, "project")
