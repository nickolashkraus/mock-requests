import unittest
from unittest.mock import Mock, patch

from requests.exceptions import HTTPError

from .. import main


class MainTestCase(unittest.TestCase):
    def setUp(self):
        super(MainTestCase, self).setUp()
        self.mock_requests = patch.object(main, "requests").start()
        self.mock_requests.get.return_value = Mock(
            status_code=200, content=b"data"
        )
        self.url = "https://static-website.com/"

    def test_main(self):
        resp = main.main()
        self.mock_requests.get.assert_called_with(self.url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(b"data", resp.content)

    def test_raise_http_error(self):
        mock_resp = Mock(
            status_code=400, content=b"error"
        )
        mock_resp.raise_for_status.side_effect = HTTPError(
            f"400 Client Error: Bad Request for url: {self.url}"
        )
        self.mock_requests.get.return_value = mock_resp
        with self.assertRaises(HTTPError) as context:
            resp = main.main()
            self.mock_requests.get.assert_called_with(self.url)
            self.assertEqual(400, resp.status_code)
            self.assertEqual(b"error", resp.content)
        self.assertEqual(
            f"400 Client Error: Bad Request for url: {self.url}",
            str(context.exception)
        )
