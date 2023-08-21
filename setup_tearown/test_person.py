import unittest
from person import Person


class PersonTest(unittest.TestCase):
    # setup runs befor mehtods, 
    # tearDown runs after mehtods,

    # both above <>class with @classmethod runs befor and after class



    def setUp(self):
        self.p1 = Person('mahdi', 'panahi')
        self.p2 = Person('mehran', 'panahi')

    
    def tearDown(self):
        print('Done.')



    def test_fullname(self):
        self.assertEqual(self.p1.fullname(), 'mahdi panahi')
        self.assertEqual(self.p2.fullname(), 'mehran panahi')


    def test_email(self):
        self.assertEqual(self.p1.email(), 'mahdipanahi@email.com')
        self.assertEqual(self.p2.email(), 'mehranpanahi@email.com')



if __name__ == "__name__":
    unittest.main()