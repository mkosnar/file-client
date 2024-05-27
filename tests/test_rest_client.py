import json
import unittest

import httpretty
from requests.exceptions import HTTPError

from clients.rest_client import RestClient


class TestRestClientStat(unittest.TestCase):

    def setUp(self):
        self.uuid = 'a1b2c3'
        self.base_url = 'http://localhost/'
        self.client = RestClient(self.base_url)

    @httpretty.activate(allow_net_connect=False)
    def test_not_found(self):
        httpretty.register_uri(httpretty.GET, f'{self.base_url}file/{self.uuid}/stat', status=404)

        with self.assertRaises(HTTPError):
            self.client.stat(self.uuid)

    @httpretty.activate(allow_net_connect=False)
    def test_found(self):
        body = {'a': 1, 'b': '2'}
        httpretty.register_uri(httpretty.GET, f'{self.base_url}file/{self.uuid}/stat', body=json.dumps(body))

        received_body = self.client.stat(self.uuid)
        self.assertDictEqual(body, received_body)


class TestRestClientRead(unittest.TestCase):

    def setUp(self):
        self.uuid = 'a1b2c3'
        self.base_url = 'http://localhost/'
        self.client = RestClient(self.base_url)

    @httpretty.activate(allow_net_connect=False)
    def test_not_found(self):
        httpretty.register_uri(httpretty.GET, f'{self.base_url}file/{self.uuid}/read', status=404)

        with self.assertRaises(HTTPError):
            self.client.read(self.uuid)

    @httpretty.activate(allow_net_connect=False)
    def test_found(self):
        body = b'abc\ndef\n'
        httpretty.register_uri(httpretty.GET, f'{self.base_url}file/{self.uuid}/read', body=body)

        received_body = self.client.read(self.uuid)
        self.assertEqual(body, received_body)
