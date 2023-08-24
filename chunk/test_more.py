from unittest import TestCase
import more
import traceback

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
