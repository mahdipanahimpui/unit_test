# pip install nose
# to run all test in directory, run:
# nosetests

# to run sepcific test file run:(-v means verbose)
# nosetests -v test_one.py 

import one

def test_add():
    assert one.add(3, 7) == 10
    assert one.add(3, -4) == -1


def test_division():
    assert one.division(4, 2) == 2



## nose testing framework no longer supported for >=python3.9