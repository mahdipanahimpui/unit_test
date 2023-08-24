from itertools import islice
from functools import partial
from collections.abc import Sequence
from collections import deque

l = [1, 2, 3, 4, 5, 6, 7]
_marker = object()
e = []

def take(iterable, n):
    return list(islice(iterable, n))

# print(take(l, 2)) # [1, 2]


# iter(iterable) => iterator
# iter(iterable, sentinel) => iterator, until the iterable should be as same as sentinel, iterate is doing

def chunked(iterable, n, strict=False):
    iterator = iter(partial(take, iter(iterable), n), [])
    if strict:
        if n is None:
            raise ValueError('n cant be None when strict is true')
        
        def ret():
            for chunk in iterator: # for parts
                if len(chunk) != n:
                    raise ValueError('iterator is not divisible by n')
                yield chunk

        return iter(ret())

    return iterator
# print(list(chunked(l, 3, True)))


# ------------------------------------------------


def first(iterable, default=_marker):
    try:
        return next(iter(iterable))
    except StopIteration as e:
        if default is _marker: # if default not sent
            raise ValueError('first() called on empty iterable') from e
        return default # default action
    

# print(first([]))
# print(first([], 'hello'))




# ------------------------------------------------------

# last:

def last(iterable, default=_marker):
    try:
        if isinstance(iterable, Sequence): # IndexError
            return iterable[-1]
        elif hasattr(iterable, '__reversed__'):
            return next(reversed(iterable)) # StopIteration
        else:
            return deque(iterable, maxlen=1)[-1] # TypeError
        
    except (IndexError, TypeError, StopIteration):

        if default is _marker:
            raise ValueError(
                'last() was called on empty iterable' 
            )
        
        return default
    

