import unittest
from main import rm
import os
from unittest import mock


class TestRm(unittest.TestCase):
    filename = 'a.txt'

    @mock.patch('main.os.remove') # mock th remove method of os from the main moudule (main is important)
    def test_rm(self, mock_rm):
        rm(self.filename)
        self.assertFalse(os.path.isfile(self.filename))