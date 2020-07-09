from unittest.mock import Mock

from dpm.tests.bdd.mocks.document_mock import DocumentMock


class FirestoreClientMock(Mock):
    def document(self, v):
        return DocumentMock()