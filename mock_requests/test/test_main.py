import unittest
from unittest.mock import Mock, patch

from .. import main

class MainTestCase(unittest.TestCase):
    def setUp(self):
        super(MainTestCase, self).setUp()
        self.mock_requests = patch.object(main, 'requests').start()
        self.mock_requests.get.return_value = Mock(
            status_code=200, content=b'data'
        )

    def test_main(self):
        mock_resp = main.main()
        self.mock_requests.get.assert_called_with(
            'https://static-website.com/'
        )
        self.assertEqual(200, mock_resp.status_code)
        self.assertEqual(b'data', mock_resp.content)
