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





# --------------------------------------------------
# always_iterable: returns an iterable

def always_iterable(obj, base_type=(str, bytes)):
    if obj is None:
        return iter(())
        # checks the isinstance in all element of base_type
    if (base_type is not None) and isinstance(obj, base_type):
        return iter((obj,))
    

    try:
        return iter(obj)
    except TypeError:
        return iter((obj,))
    

# print(list(always_iterable(1)))




# --------------------------------------------------
# split after some action

def split_after(iterable, pred, max_split=-1):
    if max_split == 0:
        yield list(iterable)
        return
    

    buf = []
    it = iter(iterable)
    
    for item in it:
        buf.append(item)

        if pred(item) and buf:
            yield buf

            if max_split == 1:
                yield(list(it)) # yield the rest of the iterable, not the main
                # if befor yield(list(it)), the print(list(it)) called the raset of iterable should be [], because elements is used in print(list(it))
                return
            buf = []
            max_split -= 1
        
    if buf:
        yield buf



# w = 'csxfexfasexfsx'
# print(list(split_after(w, lambda s: s == 'x', max_split=1)))


#------------------------------------------------------------
# split inoto sizes in a iterable

def split_into(iterable, sizes):
    it = iter(iterable)
    
    for size in sizes:
        if size is None:
            yield list(it) # yielding the rest of it that is not iterated
            return
        else:
            yield list(islice(it, size)) # islice done on rest of it thet is not iterated



# iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# iterable = []
# sizes = [2, 3, None, 2]
# actual = list(split_into(iterable, sizes))
# print(actual)



# -------------------------------------------------------------------------
# map if: if pred ok next func, else next of next func

def map_if(iterable, pred, func, func_else=lambda x:x):
    for item in iterable:
        yield func(item) if pred(item) else func_else(item)



# iterable = list(range(-5,6))
# actual = list(map_if(iterable, lambda x: x > 3, lambda x: 'toobig'))
# expected = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 'toobig']
# print(actual)

# -----------------------------------------------------------------
# time limited: limit time for and iterate an iterable

from time import monotonic
from time import sleep
# monotnic not effected from the summer clock

class time_limited:
    def __init__(self, limit_seconds, iterable):
        if limit_seconds < 0:
            raise ValueError('limit_seconds must be positive')
        
        self.limit_seconds = limit_seconds
        self._iterable = iter(iterable)
        self._start_time = monotonic()
        self.timeout = False

    def __iter__(self):
        return self
    
    def __next__(self):
        item = next(self._iterable)
        if monotonic() - self._start_time > self.limit_seconds:
            self.timeout = True
            raise StopIteration
        
        return item
    
def gen():
    sleep(0.2)
    yield 1
    yield 2
    sleep(0.8) 
    yield 3
    sleep(0.2)
    yield 4
# print(list(time_limited(1, gen())))



# ----------------------------------------------------------
# difference

from operator import sub
from itertools import tee
from itertools import starmap
from itertools import accumulate

def difference(iterable, func=sub, *, initial=None): # * means after *, all params should be key, value
    a, b = tee(iterable)

    try:
        first = [next(b)]
    except StopIteration:
        return iter([])
    
    if initial is not None:
        first = []

    return chain(first, starmap(func, zip(b, a))) # b is iterate 

# print([2,3,7])

print(list(accumulate([2, 3, 7], initial=200))) # [100, 102, 105, 112]

print(list(difference([100, 102, 105, 112], sub, initial=1)))





# -------------------------------------------------------------------------

# value chain:

def value_chain(*args):
    for value in args:
        if isinstance(value, (str, bytes)):
            yield value
            continue
        try:
            yield from value # if args element are iterabel, iterate in inner of them
        except TypeError: # if inner is not iterable 
            yield value 





#---------------------------------------------------------------------

# sequence_view: act as sequence

class SequenceView(Sequence):
    def __init__(self, target):
        if not isinstance(target, Sequence):
            raise TypeError
        self._target = target

    def __getitem__(self, index):
        return self._target[index]
    
    def __len__(self):
        return len(self._target)
    

    def __repr__(self):
        return f'{self.__class__.__name__}({self._target})'



