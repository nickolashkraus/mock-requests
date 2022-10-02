import unittest
from unittest.mock import Mock, call, patch

from requests.exceptions import HTTPError

from .. import main


class MainTestCase(unittest.TestCase):
    def setUp(self):
        super(MainTestCase, self).setUp()
        self.mock_requests = patch.object(main, "requests").start()
        self.url = "https://static-website.com"
        self.data = [{"a": "b"}]

    def test_resp(self):
        self.mock_requests.get.return_value = Mock(status_code=200, content=b"data")
        ret = main.resp()
        self.mock_requests.get.assert_called_with(self.url)
        self.assertEqual(200, ret.status_code)
        self.assertEqual(b"data", ret.content)

    def test_text(self):
        self.mock_requests.get.return_value = Mock(status_code=200, text="data")
        ret = main.text()
        self.mock_requests.get.assert_called_with(self.url)
        self.assertEqual("data", ret)

    def test_json(self):
        self.mock_requests.get.side_effect = [
            Mock(status_code=200, json=Mock(return_value=self.data[0]))
        ]
        ret = main.json()
        self.mock_requests.get.assert_has_calls([call(self.url)])
        self.assertEqual(self.data[0], ret)

    def test_auth(self):
        auth = Mock(username="user", password="password")
        mock_basic_auth = patch.object(main.requests.auth, "HTTPBasicAuth").start()
        mock_basic_auth.return_value = auth
        self.mock_requests.get.side_effect = [
            Mock(status_code=200, json=Mock(return_value=self.data[0]))
        ]
        ret = main.auth()
        self.mock_requests.get.assert_has_calls([call(self.url, auth=auth)])
        self.assertEqual(self.data[0], ret)

    def test_raise_http_error(self):
        mock_resp = Mock(status_code=400, content=b"error")
        mock_resp.raise_for_status.side_effect = HTTPError(
            f"400 Client Error: Bad Request for url: {self.url}"
        )
        self.mock_requests.get.return_value = mock_resp
        with self.assertRaises(HTTPError) as context:
            ret = main.resp()
            self.mock_requests.get.assert_called_with(self.url)
            self.assertEqual(400, ret.status_code)
            self.assertEqual(b"error", ret.content)
        self.assertEqual(
            f"400 Client Error: Bad Request for url: {self.url}", str(context.exception)
        )
