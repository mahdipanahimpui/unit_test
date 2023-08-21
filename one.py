 # run the:
# python -m doctest -v one.py
# -v (verbose) option



# in module level testing
"""
>>> add(5, 1)
6
"""


# run the 
def add(x, y):
    """
    >>> add(7, 6)
    13
    >>> add(2,-7)
    -5
    """
    return x + y
