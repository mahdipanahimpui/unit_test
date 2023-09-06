import unittest
from unittest import mock
from requests.exceptions import Timeout
from main import get_apple, requests



class TestApple(unittest.TestCase):


    # @mock.patch('main.requests') # call the request of main (main is important)
    # def test_get_apple_timeout(self, mock_requests):  # an arg is sent by patch
    #     mock_requests.get.side_effect = Timeout
    #     with self.assertRaises(Timeout):
    #         get_apple()




    # if you want to mock just a method use @mock.patch.object
    # could decalre the side effect in params of @mock.... decorator, if not 

    @mock.patch.object(requests, 'get', side_effect=Timeout) # IMPORTANT: request is imported form main.py. method name as string
    def test_get_apple_timeout(self, mock_request): # getting param is important
        with self.assertRaises(Timeout):
            get_apple()
