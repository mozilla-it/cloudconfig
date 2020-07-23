from unittest.mock import Mock


class MockEnv(Mock):
    doc_data = dict()

    def insert_property(self, key, value):
        MockEnv.doc_data.update({key: value})
