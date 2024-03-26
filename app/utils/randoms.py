


import random
import string


def generate_account_number():
    """ Generate a random account number """
    return ''.join(random.choices(string.digits, k=20))