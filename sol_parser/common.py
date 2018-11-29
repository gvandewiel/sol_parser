"""Common functions and classes"""

import unicodedata


def normalize(text):
    """Normalize a string to lowercase.

    To used when performing string comparisson
    """
    return unicodedata.normalize("NFKD", text.lower())


def str_check(str=''):
    """Replace list of characters with underscore"""
    for char in [' ', '/', '-']:
        if char in str:
            str = str.replace(char, '_')
    return str
