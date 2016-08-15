import requests
import unittest
import json

import properties


class BaseAPITestCase(unittest.TestCase):
    @staticmethod
    def testGet():
        r = requests.get(properties.apiTestingURL)
        assert r.status_code == 200
        d = json.dumps(r.json())
        assert d.__contains__('Tony')

    @staticmethod
    def testPost():
        json_string_from_file = open('jsonExample.json').read()
        j = json.loads(json_string_from_file)
        r = requests.post(properties.apiTestingURL, j)
        assert r.status_code == 405

    @staticmethod
    def testJsonPost():
        r = requests.delete(properties.apiTestingURL)
        assert r.status_code == 405


