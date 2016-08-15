import requests
import unittest
import json


class BaseAPITestCase(unittest.TestCase):
    @staticmethod
    def testGet():
        r = requests.get('http://127.0.0.1:8080/hello-world?name=Tony')
        assert r.status_code == 200
        d = json.dumps(r.json())
        assert d.__contains__('Tony')

    @staticmethod
    def testPost():
        json_string_from_file = open('jsonExample.json').read()
        j = json.loads(json_string_from_file)
        r = requests.post('http://127.0.0.1:8080/hello-world?name=Tony', j)
        assert r.status_code == 405

    @staticmethod
    def testJsonPost():
        r = requests.delete('http://127.0.0.1:8080/hello-world?name=Tony')
        assert r.status_code == 405


