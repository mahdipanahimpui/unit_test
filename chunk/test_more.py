from unittest import TestCase
import more


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
    