from itertools import islice
from functools import partial


l = [1, 2, 3, 4, 5, 6, 7]


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