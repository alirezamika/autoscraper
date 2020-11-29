from collections import OrderedDict

import random
import string
import unicodedata

from difflib import SequenceMatcher


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


def get_non_rec_text(element):
    return ''.join(element.find_all(text=True, recursive=False)).strip()


def normalize(item):
    if not isinstance(item, str):
        return item
    return unicodedata.normalize("NFKD", item.strip())


def text_match(t1, t2, ratio_limit):
    if hasattr(t1, 'fullmatch'):
        return bool(t1.fullmatch(t2))
    if ratio_limit >= 1:
        return t1 == t2
    return SequenceMatcher(None, t1, t2).ratio() >= ratio_limit


class ResultItem():
    def __init__(self, text, index):
        self.text = text
        self.index = index

    def __str__(self):
        return self.text


class FuzzyText(object):
    def __init__(self, text, ratio_limit):
        self.text = text
        self.ratio_limit = ratio_limit
        self.match = None

    def search(self, text):
        return SequenceMatcher(None, self.text, text).ratio() >= self.ratio_limit
