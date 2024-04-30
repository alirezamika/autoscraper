from collections import OrderedDict
import random
import string
import unicodedata
from difflib import SequenceMatcher
from typing import List, Union

def unique_stack_list(stack_list: List[dict]) -> List[dict]:
    """
    Remove duplicate stacks from the list while preserving order.

    Args:
        stack_list (List[dict]): List of stacks, where each stack is a dictionary.

    Returns:
        List[dict]: List of unique stacks.
    """
    seen = set()
    unique_list = []
    for stack in stack_list:
        stack_hash = stack.get('hash')  # Better to use get() to avoid KeyErrors
        if stack_hash in seen:
            continue
        unique_list.append(stack)
        seen.add(stack_hash)
    return unique_list


def unique_hashable(hashable_items: List[Union[str, int]]) -> List[Union[str, int]]:
    """
    Remove duplicate hashable items from the list while preserving order.

    Args:
        hashable_items (List[Union[str, int]]): List of hashable items.

    Returns:
        List[Union[str, int]]: List of unique hashable items.
    """
    return list(OrderedDict.fromkeys(hashable_items))


def get_random_str(n: int) -> str:
    """
    Generate a random string of lowercase letters and digits.

    Args:
        n (int): Length of the random string.

    Returns:
        str: Random string.
    """
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(n))


def get_non_rec_text(element) -> str:
    """
    Extract non-recursive text from an HTML element.

    Args:
        element: HTML element.

    Returns:
        str: Non-recursive text.
    """
    return ''.join(element.find_all(text=True, recursive=False)).strip()


def normalize(item: Union[str, Any]) -> Union[str, Any]:
    """
    Normalize a string by stripping and converting to NFKD form.

    Args:
        item (Union[str, Any]): Input item.

    Returns:
        Union[str, Any]: Normalized item.
    """
    if not isinstance(item, str):
        return item
    return unicodedata.normalize("NFKD", item.strip())


def text_match(t1: str, t2: str, ratio_limit: float) -> bool:
    """
    Check if two texts match with a given ratio limit.

    Args:
        t1 (str): First text.
        t2 (str): Second text.
        ratio_limit (float): Similarity ratio limit.

    Returns:
        bool: True if the texts match, False otherwise.
    """
    if hasattr(t1, 'fullmatch'):
        return bool(t1.fullmatch(t2))
    if ratio_limit >= 1:
        return t1 == t2
    return SequenceMatcher(None, t1, t2).ratio() >= ratio_limit


class ResultItem:
    def __init__(self, text: str, index: int) -> None:
        """
        Initialize a ResultItem object.

        Args:
            text (str): Text content.
            index (int): Index of the item.
        """
        self.text = text
        self.index = index

    def __str__(self) -> str:
        """
        Convert ResultItem object to a string.

        Returns:
            str: String representation of the object.
        """
        return self.text


class FuzzyText:
    def __init__(self, text: str, ratio_limit: float) -> None:
        """
        Initialize a FuzzyText object.

        Args:
            text (str): Text content.
            ratio_limit (float): Similarity ratio limit.
        """
        self.text = text
        self.ratio_limit = ratio_limit
        self.match = None

    def search(self, text: str) -> bool:
        """
        Search for a text with a similarity ratio above the limit.

        Args:
            text (str): Text to compare.

        Returns:
            bool: True if a match is found, False otherwise.
        """
        return SequenceMatcher(None, self.text, text).ratio() >= self.ratio_limit
