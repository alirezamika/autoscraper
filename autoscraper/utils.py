from collections import OrderedDict

import random
import string


def unique_stack_list(stack_list):
    seen = set()
    unique_list = []
    for stack in stack_list:
        stack_hash = stack['hash']
        if stack_hash in seen:
            continue
        unique_list.append(stack)
        seen.add(stack_hash)
    return unique_list


def unique_hashable(hashable_items):
    """Removes duplicates from the list. Must preserve the orders."""
    return list(OrderedDict.fromkeys(hashable_items))


def get_random_str(n):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for i in range(n))


class ResultItem():
    def __init__(self, text, index):
        self.text = text
        self.index = index

    def __str__(self):
        return self.text
