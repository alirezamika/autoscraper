import random
import string


def unique(item_list):
    return list(set(item_list))

def get_random_str(n):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for i in range(n))
