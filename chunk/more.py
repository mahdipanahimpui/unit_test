from itertools import islice
from functools import partial
from collections.abc import Sequence
from collections import deque

l = [0, 1, 2, 3, 4, 5, 6, 7]
s = ['a', 'b', 'c', 'd']
_marker = object()
e = []

def take(iterable, n):
    return list(islice(iterable, n))

# print(take(l, 2)) # [1, 2]


# iter(iterable) => iterator
# iter(iterable, sentinel) => iterator, until the iterable should be as same as sentinel, iterate is doing

# chunk an iterable, strict true, is for dividabel chunk
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

# returns the first of iterable if not exists returns default
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

# last: returns the nth item of not found default returns

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
    


def nth_or_last(iterable, n, default=_marker):
    return last(islice(iterable, n+1), default=default)

# print(last(e, 3), )


# ---------------------------------------------------------
# an iterable just have 1 element not less or more

def one(iterable, too_short=None, too_long=None):
    it = iter(iterable)
    try:
        first_value = next(it)
    except StopIteration as e:
        raise (
            too_short or ValueError('too few items in iterable (expected 1)')
        ) from e # stop iteration error printed too, beacuse of __cause__
    
    try:
        second_value = next(it)
    except StopIteration:
        pass
    else:
        msg = (
            'Expected exactly one item in iterable, but got {}, {}, '
            'and perhaps more.'.format(first_value, second_value)
        )
        raise too_long or ValueError(msg)
    return first_value





# --------------------------------------------------------------

# interLeave

# join many iterable zigzagi based on shortest list
from itertools import chain

def interleave(*iterable): # * means many iterable is passed iterable=(iterable, iterable, ..)
    return chain.from_iterable(zip(*iterable)) # *iterable=iterable iterable ...    * used to unpack
    # returns an itertool.chain object use list to see


# print(list(interleave(['amri'], 'hello')))


# ----------------------------------------------------
# repeat each: repeat each element of iterabel
from itertools import cycle, repeat

def repeat_each(iterable, n=2):
    return chain.from_iterable(map(repeat, iterable, repeat(n))) # in each map send the n as param, by repeat(n), Note: repeat is lazy


# print(list(repeat_each(s)))




# ------------------------------------------------------

# strictly_n: check that the len of iterable == n

def raise_(exception, *args):
    raise exception(*args)


def strictly_n(iterable, n, too_short=None, too_long=None):
    if too_short is None:
        too_short = lambda item_count: raise_(
            ValueError,
            f'Too few items in iterable (got {item_count})'
        )

    if too_long is None:
        too_long = lambda item_count: raise_(
            ValueError,
            f'Too many items in iterable (got at least {item_count})'
        )

    it = iter(iterable)
    
    for i in range(n):
        try:
            item = next(it)
        except StopIteration:
            too_short(i)
            return  # returns None
        else:
            yield item

    try: 
        next(it)
    except StopIteration:
        pass
    else:
        too_long(n+1)


# print(list(strictly_n(s, 4)))



# ----------------------------------------------
# only: check the iterable just have one element

def only(iterable, default=None, too_long=None):
    it = iter(iterable)
    first_value = next(it, default)

    try:
        second_value = next(it)
    except StopIteration:
        pass
    else:
        msg = (
            'Expected exactly one element. '
            'got {},{}'.format(first_value, second_value)
        )

        raise too_long or ValueError(msg)
    return first_value


# -------------------------------------------------------

# always_reversible: returns the reversed of iterables, not changes the main

def always_reversible(iterable):
    try:
        return reversed(iterable)
    except TypeError:
        return reversed(list(iterable))


# print(list(always_reversible(l)))





# -------------------------------------------------------


