import base64
import json


class MockData:
    def __init__(self):
        global test_key, test_value
        val = base64.b64encode(test_value.encode('ascii'))
        vdict = {test_key: val.decode()}
        val1 = json.dumps(vdict)
        self.data = val1.encode("utf-8")