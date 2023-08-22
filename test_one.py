import pytest
import one



class TestOne:
    def test_division(self):
        assert one.division(10,2) == 5
        with pytest.raises(ZeroDivisionError):
            one.division(3, 0)


    def test_add(self):
        assert one.add(10, 2) == 12


# pytest test_one.py --resultlog=result.log