# patch, makes easier using the mock class
import requests


# in mock3 dir, run python -m unittest ./tests.py



def get_apple():
    r = requests.get('https://www.apple.com')
    return r.status_code

