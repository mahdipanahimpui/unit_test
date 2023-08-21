# unit test

# create test_<this_file_name>.py


def add(x, y):
    return x + y

def devision(x, y):
    if y == 0:
        raise ZeroDivisionError('can devide by zero')
    return x / y

