import unittest
import one



# the class name is <file_to_test>Test
class OneTest(unittest.TestCase):
    # test_<def that is going to test>
    def test_devision(self):
        self.assertEqual(one.devision(-1, 4), -.25)
        # for devisions:
        self.assertRaises(ZeroDivisionError, one.devision, 4, 0)



    def test_add(self):
        self.assertEqual(one.add(5,0), 5)    
        self.assertEqual(one.add(5,2), 7)  




if __name__ == '__name__':
    unittest.main()
    # run in terminal:
    # python -m unittest test_one.py

# to run all tests file:
# python -m unittest discover