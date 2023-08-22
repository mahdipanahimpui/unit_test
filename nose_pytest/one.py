def add(x, y):
    return x + y

def division(x, y):
    if y == 0:
        raise ZeroDivisionError('can devide by zero')
    return x / y