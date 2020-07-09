from unittest.mock import Mock


class DocumentMock(Mock):
    def on_snapshot(self, v):
        return Mock()