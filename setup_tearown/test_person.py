from person import Person
import pytest

# teardown and setup in pytest

# start of class should be Test
class TestPerson:
    @pytest.fixture
    def setup(self):
        self.p1 = Person('amir', 'big')
        self.p2 = Person('john', 'doe')
 
        # for teardown use yield '<method name>'
        yield 'setup'
        print('Done.')


    def test_fullname(self, setup):
        assert self.p1.fullname() == 'amir big'
        assert self.p2.fullname() == 'john doe'


    def test_email(self, setup):
        assert self.p1.email() == 'amirbig@email.com'
        assert self.p2.email() == 'johndoe@email.com'


