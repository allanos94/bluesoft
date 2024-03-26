import random
import string
import uuid


def generate_account_number():
    """ Generate a random account number """
    return ''.join(random.choices(string.digits, k=20))

def generate_uuid():
    """ Generate a random UUID """
    return str(uuid.uuid4())