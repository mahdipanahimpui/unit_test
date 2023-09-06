# a example of mock with apple.com

# side_effect: it is like return_value, does other action

import requests
import unittest
from unittest.mock import Mock
from requests.exceptions import Timeout

# in mock3 dir, run python -m unittest ./main.py

requests = Mock()

# simulation of Timeout exception of get request

def get_apple():
    r = requests.get('https://www.apple.com')
    return r.status_code


class TestApple(unittest.TestCase):
    def test_get_apple_timeout(self):
        requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            get_apple()