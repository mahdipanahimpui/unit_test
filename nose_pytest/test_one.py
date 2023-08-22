# pip install pytest
# to run all test in directory, run:
# pytest

# to run sepcific test file run:(-v means verbose)
# pytest -v test_one.py 

import one

# in class base test:
class TestOne:

    def test_add(self):
        assert one.add(3, 7) == 10
        assert one.add(3, -4) == -1


    def test_division(self):
        assert one.division(4, 2) == 2

