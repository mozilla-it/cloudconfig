from unittest.mock import Mock

from dpm.tests.bdd.mocks.mockx import MockX
from dpm.tests.bdd.mocks.mock_object import MockObj


class SecretManagerServiceClientMock(Mock):

    def list_secret_versions(self, x):
        return list(list(MockObj()))


    def secret_path(self, x, y):
        return Mock()


    def list_secret_versions(self, x):
        return [MockX()]


    def access_secret_version(self, p):
        return MockX()