from unittest import TestCase
import more
import traceback
from itertools import count, cycle, repeat

class TakeTests(TestCase):
    def test_simple_take(self):
        t = more.take(range(10), 5)
        self.assertEqual(t, [0,1,2,3,4])

    def test_null_take(self):
        t = more.take(range(10), 0)
        self.assertEqual(t, [])


    def test_negative_take(self):
        self.assertRaises(ValueError, lambda: more.take(-3, range(10)))

    def test_take_too_much(self):
         t = more.take(range(5), 10)
         self.assertEqual(t, [0,1,2,3,4])



class ChunkedTests(TestCase):
    
    def test_even(self):
        self.assertEqual(
            list(more.chunked('ABCDEF', 3)), [['A', 'B', 'C'], ['D', 'E', 'F']]
        )

    def test_odd(self):
        self.assertEqual(
            list(more.chunked('ABCDE', 3)), [['A', 'B', 'C'], ['D', 'E']]
        )


    def test_even(self):
        self.assertEqual(
            list(more.chunked('ABCDEF', None)), [['A', 'B', 'C', 'D', 'E', 'F']]
        )


    def test_strict_false(self):
        self.assertEqual(
            list(more.chunked('ABCDE', 3, strict=False)), 
            [['A', 'B', 'C'], ['D', 'E']]
        )

    
    def test_strict_true(self):
        def f():
            return list(more.chunked('ABCDE', 3, strict=True))
        self.assertRaisesRegex(ValueError, 'iterator is not divisible by n', f) # error should be equel the same error description
        self.assertEqual(list(more.chunked('ABCDEF', 3, strict=True)), [['A', 'B', 'C'], ['D', 'E', 'F']])


    def test_strict_true_size_none(self):
        def f():
            return list(more.chunked('ABCDE', None, strict=True))
        self.assertRaisesRegex(ValueError, 'n cant be None when strict is true', f)



class FirstTests(TestCase):
    def test_many(self):
        self.assertEqual(more.first([x for x in range(4)]), 0)

    
    def test_one(self):
        self.assertEqual(more.first([3]), 3)


    def test_default(self):
        self.assertEqual(more.first([], 'hello'), 'hello')

    
    def test_empty_stop_iteraion(self):
        try:
            more.first([])
        except ValueError:
            formatted_exc = traceback.format_exc()
            self.assertIn('StopIteration', formatted_exc) # 'StopIteration' contains in the exception
            self.assertIn('first() called on empty iterable', formatted_exc)
        else:
            self.fail() # execute if no exceptions are raised

# ------------------------------------------------------------------
# subtest
class LastTests(TestCase):
    def test_basic(self):
        cases = [
            (range(4), 3),
            (iter(range(4)), 3),
            (range(1), 0),
            ({n: str(n) for n in range(5)}, 4)

        ]

        for iterable, expected in cases:
            with self.subTest(iterable=iterable): # subtest point to wich loop error is ocured
                self.assertEqual(more.last(iterable), expected)



    def test_default(self):
        for iterable, default, expected in [
            (range(1), None, 0), 
            ([], None, None), 
            ({}, None, None),
            (iter([]), None, None)
        ]:
            with self.subTest(args=(iterable, default)): # the <args> name is what you want
                self.assertEqual(more.last(iterable, default=default), expected)


    
    def test_empty(self):
        for iterable in ([], iter(range(0))):
            with self.subTest(iterable=iterable):
                with self.assertRaises(ValueError): # <with> means test <self.assertRaises(ValueError)> with the more.last(iterable)
                    more.last(iterable)



class NthOrLastTests(TestCase):
    def test_basic(self):
        self.assertEqual(more.nth_or_last(range(3), 1), 1) 
        self.assertEqual(more.nth_or_last(range(3), 3), 2)


    def test_default_value(self):
        default = 42
        self.assertEqual(more.nth_or_last(range(0), 3, default), default)

    def test_empty_iterable_no_default(self):
        # self.assertRaises(ValueError, more.nth_or_last(range(0), 0)) # it is false, because error not returned,
        # to return error, use lambda
        self.assertRaises(ValueError, lambda: more.nth_or_last(range(0), 0))




class OneTests(TestCase):
    def test_basic(self):
        it = ['item']
        self.assertEqual(more.one(it), 'item')

    def test_short(self):
        it = []
        for too_short, exc_type in [
            (None, ValueError),
            (IndexError, IndexError)
        ]:
            with self.subTest(too_short=too_short):
                try:
                    more.one(it, too_short=too_short)
                except exc_type:
                    formatted_exc = traceback.format_exc()
                    self.assertIn('StopIteration', formatted_exc)
                    self.assertIn('The above exception was the direct cause', formatted_exc)
                
                else:
                    self.fail()

    def test_too_long(self):
        it = count() # just count(by next()) from 0 to unlimit,
        self.assertRaises(ValueError, lambda: more.one(it))
        self.assertEqual(next(it), 2)
        self.assertRaises(
            OverflowError, lambda: more.one(it, too_long=OverflowError)
        )

    def test_too_long_default_message(self):
        it = count()
        self.assertRaisesRegex(
            ValueError, 
            'Expected exactly one item in iterable, but got 0, 1, and perhaps more.',
            lambda: more.one(it)
        )




class InterLeaveTests(TestCase):
    def test_even(self):
        actual = list(more.interleave([1, 2], [3, 4]))
        expected = [1, 3, 2, 4]
        self.assertEqual(actual, expected)


    def test_short(self):
        actual = list(more.interleave([1, 2, 3], [4, 5]))
        excepted = [1, 4, 2, 5]
        self.assertEqual(actual, excepted)


    def test_mixed_types(self):
        it_list = ['a', 'b', 'c']
        it_str = '1234'
        it_inf = count() #NOTE: every iterator is a iterable but not inverse
        actual = list(more.interleave(it_list, it_str, it_inf))
        expected = ['a', '1', 0, 'b', '2', 1, 'c', '3', 2]
        self.assertEqual(actual, expected)




class RepeatEachTests(TestCase):
    def test_default(self):
        actual = list(more.repeat_each('abc'))
        excepted = ['a', 'a', 'b', 'b', 'c', 'c']
        self.assertEqual(actual, excepted)

    def test_basic(self):
        actual = list(more.repeat_each('abc', 3))
        expected = ['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'c']
        self.assertEqual(actual, expected)


    def test_no_repeat(self):
        actual = list(more.repeat_each('abc', 0))
        expected = []
        self.assertEqual(actual, expected)

    
    def test_empty(self):
        actual = list(more.repeat_each(''))
        expected = []
        self.assertEqual(actual, expected)


    def test_negative_repeat(self):
        actual = list(more.repeat_each('abc', -1))
        expected = []
        self.assertEqual(actual, expected) 

            
    def test_infinite_input(self):
        repeator = more.repeat_each(cycle('ab')) # cycle is lazy, works by next
        actual = more.take(repeator, 6) 
        expected = ['a', 'a', 'b', 'b', 'a', 'a']
        self.assertEqual(actual, expected)




class StrictlyNTests(TestCase):
    def test_basic(self):
        iterable = ['a', 'b', 'c']
        n = 3
        actual = list(more.strictly_n(iterable, n))
        expected = iterable
        self.assertEqual(actual, expected)


    def test_too_many_default(self):
        iterable = ['a', 'b', 'c']
        n = 4
        with self.assertRaises(ValueError) as exc:
            list(more.strictly_n(iterable, n))

        self.assertEqual(
            'Too few items in iterable (got 3)', exc.exception.args[0]
        )

    
    def test_too_long_default(self):
        iterable = ['a', 'b', 'c']
        n = 2
        with self.assertRaises(ValueError) as exc:
            list(more.strictly_n(iterable, n))

        self.assertEqual(
            'Too many items in iterable (got at least 3)', exc.exception.args[0]
        )

    
    def test_too_short_custom(self):
        call_count = 0
        def too_short(item_count):
            nonlocal call_count
            call_count += 1
        
        iterable = ['a', 'b', 'c', 'd']
        n = 6
        actual = []

        for item in more.strictly_n(iterable, n, too_short=too_short):
            actual.append(item)
        expected = ['a', 'b', 'c', 'd']
        self.assertEqual(actual, expected)
        self.assertEqual(call_count, 1)



    def test_too_long_custom(self):
        import logging
        
        iterable = ['a', 'b', 'c', 'd']
        n = 2
        too_long = lambda item_count: logging.warning(
            f'picked the {n} items'
        )

        with self.assertLogs(level='WARNING') as exc:
            actual = list(more.strictly_n(iterable, n, too_long=too_long))

        self.assertEqual(actual, ['a', 'b'])
        self.assertIn('picked the 2 items', exc.output[0])





class OnlyTests(TestCase):
    def test_defaults(self):
        self.assertEqual(more.only([]), None)
        self.assertEqual(more.only([1]), 1)
        self.assertRaises(ValueError, lambda: more.only([1, 2])) # lambda returns the exceptions

    def test_custom_value(self):
        self.assertEqual(more.only([], default='!'), '!')
        self.assertEqual(more.only([1], default='!'), 1)
        self.assertRaises(ValueError, lambda: more.only([1,2], default='!'))


    def test_custom_exception(self):
        self.assertEqual(more.only([], too_long=RuntimeError), None)
        self.assertEqual(more.only([1], too_long=RuntimeError), 1)
        self.assertRaises(RuntimeError, lambda: more.only([1,2], too_long=RuntimeError))


    def test_default_exception_message(self):
        self.assertRaisesRegex(
            ValueError,
            "Expected exactly one element. got foo,boo",
            lambda: more.only(['foo', 'boo', 'bar'])
        
        )



class AlwaysReversibelTests(TestCase):
    def test_regular_reversed(self):
        self.assertEqual(
            list(reversed(range(10))), list(more.always_reversible(range(10)))
        )
        
        self.assertEqual(
            list(reversed([1,2,3])), list(more.always_reversible([1,2,3]))
        )

        self.assertEqual(
            reversed([1,3,4]).__class__, more.always_reversible([1,2,3]).__class__
        )

    def test_nonseq_reversed(self):
        self.assertEqual( # sending an generator: always_reversible(x for x in range(10)
            list(reversed(range(10))), list(more.always_reversible(x for x in range(10)))
        )

        self.assertEqual( # sending an generator: always_reversible(x for x in range(10)
            list(reversed([1, 2, 3])), list(more.always_reversible(x for x in [1,2,3]))
        )

        self.assertNotEqual(
            # generator != list
            reversed((1,2)).__class__, more.always_reversible(x for x in (1,2)).__class__
        )



class AlwaysIterableTests(TestCase):
    def test_singel(self):
        self.assertEqual(list(more.always_iterable(1)), [1])

    def test_string_byte(self):
        # b in b'bar' means byte
        for obj in ['foo', b'bar', 'baz']:
            actual = list(more.always_iterable(obj))
            excepted = [obj]
            self.assertEqual(actual, excepted)

    def test_base_type(self):
        dict_obj = {'a':1, 'b':2}
        str_obj = '123'

        default_actual = list(more.always_iterable(dict_obj))
        default_expected = list(dict_obj)
        self.assertEqual(default_actual, default_expected)


        custom_acutal = list(more.always_iterable(dict_obj, base_type=dict))
        custom_expected = [dict_obj]
        self.assertEqual(custom_acutal, custom_expected)

        str_actual = list(more.always_iterable(str_obj, base_type=None))
        str_expected = list(str_obj)
        self.assertEqual(str_actual, str_expected)

        base_type = ((dict,),)
        custom_actual = list(more.always_iterable(dict_obj, base_type=base_type))
        custom_expected = [dict_obj]
        self.assertEqual(custom_actual, custom_expected)


    def test_iterables(self):
        self.assertEqual(list(more.always_iterable([0,1])), [0,1])
        self.assertEqual(list(more.always_iterable([0,1], base_type=list)), [[0,1]])
        self.assertEqual(list(more.always_iterable(iter('foo'))), ['f', 'o', 'o'])
        self.assertEqual(list(more.always_iterable([])), [])


    def test_generator(self):
        def _gen():
            yield 0
            yield 1
        self.assertEqual(list(more.always_iterable(_gen())), [0,1])





class TestSplitAfter(TestCase):
    def test_start_with_sep(self):
        actual = list(more.split_after('xooxoo', lambda c: c == 'x'))
        expected = [['x'], ['o', 'o', 'x'], ['o', 'o']]
        self.assertEqual(actual, expected)

    def test_ends_with_sep(self):
        actual = list(more.split_after('ooxoox', lambda c: c == 'x'))
        expected = [['o', 'o', 'x'], ['o', 'o', 'x']]
        self.assertEqual(actual, expected)


    def test_no_sep(self):
        actual = list(more.split_after('ooo', lambda c: c == 'x'))
        expected = [['o', 'o', 'o']]
        self.assertEqual(actual, expected)


    def test_max_split(self):
        for args, expected in [
            (
                ('a,b,c,d', lambda c: c == ',', -1),
                [['a', ','], ['b', ','], ['c', ','], ['d']]
            ),

            (
                ('a,b,c,d', lambda c: c == ',', 0),
                [['a', ',', 'b', ',', 'c', ',', 'd']]
            ),

            (
                ('a,b,c,d', lambda c: c == ',', 1),
                [['a', ','], ['b', ',', 'c', ',', 'd']]
            ),

            (
                ('a,b,c,d', lambda c: c == ',', 2),
                [['a', ','], ['b', ','], ['c', ',', 'd']]
            )


        ]:
            actual = list(more.split_after(*args)) # * used to open the tuple
            self.assertEqual(actual, expected)



class SplitIntoTests(TestCase):
    def test_iterable_just_right(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = [2, 3, 4]
        expected = [
            [1, 2],
            [3, 4, 5],
            [6, 7, 8, 9]
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)

    
    def test_iterable_too_small(self):
        iterable = [1, 2, 3, 4, 5, 6, 7]
        sizes = [2, 3, 4]
        expected = [
            [1, 2],
            [3, 4, 5],
            [6, 7]
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)



    def test_iterable_too_small_extra(self):
        iterable = [1, 2, 3, 4, 5, 6, 7]
        sizes = [2, 3, 4, 5]
        expected = [
            [1, 2],
            [3, 4, 5],
            [6, 7],
            []
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)



    def test_iterable_too_large(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = [2, 3, 2]
        expected = [
            [1, 2],
            [3, 4, 5],
            [6, 7]
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)


    def test_iterable_using_none_with_leftover(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = [2, 3, None]
        expected = [
            [1, 2],
            [3, 4, 5],
            [6, 7, 8, 9]
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)


    def test_iterable_using_none_without_leftover(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = [2, 3, 4, None]
        expected = [
            [1, 2],
            [3, 4, 5],
            [6, 7, 8, 9],
            []
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)



    def test_iterable_using_none_mid_sizes(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = [2, 3, None, 2]
        expected = [
            [1, 2],
            [3, 4, 5],
            [6, 7, 8, 9]
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)



    def test_iterable_empty(self):
        iterable = []
        sizes = [2, 3, 2]
        expected = [
            [],
            [],
            []
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)



    def test_iterable_empty_using_none(self):
        iterable = []
        sizes = [2, 4, None, 3]
        expected = [
            [],
            [],
            []
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)



    def test_sizes_empty(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = []
        expected = []
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)


    def test_sizes_both_empty(self):
        iterable = []
        sizes = []
        expected = []
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)


    def test_bool_sizes(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = [3, True, 2, False] # True = 1, False = 0
        expected = [[1, 2, 3], [4], [5, 6], []]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)


    def test_invalid_in_sizes(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = [1, [], 3]
        with self.assertRaises(ValueError):
            list(more.split_into(iterable, sizes))


    def test_invalid_in_sizes_after_none(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = [2, 3, None, 2, []]
        expected = [
            [1, 2],
            [3, 4, 5],
            [6, 7, 8, 9]
        ]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)


    def test_genarator_iterable_ingegrity(self):
        iterable = (i for i in range(10))
        sizes = [2, 3]
        expected = [[0,1], [2,3,4]]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, expected)

        iterable_expected = [5, 6, 7, 8, 9]
        iterable_actual = list(iterable)
        self.assertEqual(iterable_actual, iterable_expected)

    
    def test_generator_sizes_integrity(self):
        iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sizes = (i for i in [1, 2, None, 3, 4])
        excepted = [[1], [2,3], [4,5,6,7,8,9]]
        actual = list(more.split_into(iterable, sizes))
        self.assertEqual(actual, excepted)

        sizes_expected = [3, 4]
        sizes_actual = list(sizes)
        self.assertEqual(sizes_expected, sizes_actual)




class MapIfTests(TestCase):
    def test_without_func_else(self):
        iterable = list(range(-5,6))
        actual = list(more.map_if(iterable, lambda x: x > 3, lambda x: 'toobig'))
        expected = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 'toobig', 'toobig']


    def test_with_func_else(self):
        iterable = list(range(-5,5))
        actual = list(more.map_if(iterable, lambda x: x >= 0, lambda x: 'notneg', lambda x: 'neg'))
        expected = ['neg'] * 5 + ['notneg'] * 5
        self.assertEqual(actual, expected)


    def test_empty(self):
        actual = list(more.map_if([], lambda x: len(x) > 5, lambda x: None))
        excepted = []
        self.assertEqual(actual, excepted)



from time import sleep

class TimeLimitedTests(TestCase):

    def test_basic(self):

        def generator():
            yield 1
            yield 2
            sleep(0.2)
            yield 3
        
        iterable = more.time_limited(0.1, generator())
        actual = list(iterable)
        excepted = [1, 2]
        self.assertEqual(actual, excepted)
        self.assertTrue(iterable.timeout)


    def test_complete(self):
        iterable = more.time_limited(2, iter(range(10)))
        actual = list(iterable)
        excepted = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(actual, excepted)
        self.assertFalse(iterable.timeout)

    def test_ziro_limit(self):
        iterable = more.time_limited(0, count())
        actual = list(iterable)
        excepted = []
        self.assertEqual(actual, excepted)
        self.assertTrue(iterable.timeout)


    def test_invalid_limit(self):
        with self.assertRaises(ValueError):
            list(more.time_limited(-0.1, count()))


    