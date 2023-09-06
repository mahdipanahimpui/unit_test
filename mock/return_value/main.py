import datetime
from unittest.mock import Mock

# example of return value in mock


# befor mock the datetime is the real
tuesday = datetime.datetime(year=2019, month=1, day=1)
sunday = datetime.datetime(year=2019, month=1, day=6)


datetime = Mock() # the name must be as same as the module that is used

def is_weekday():
    today = datetime.datetime.today()
    return (0 <= today.weekday() < 6)  # is weekdaty is 6 returns False



# change the returned value of datetime.datetime.today.
datetime.datetime.today.return_value = tuesday

# test:
assert is_weekday() # no assertion error


datetime.datetime.today.return_value = sunday

# test:
assert is_weekday() # assertion error
