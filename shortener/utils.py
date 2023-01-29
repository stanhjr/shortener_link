from random import choice

from string import ascii_letters, digits

from django.conf import settings

SIZE = getattr(settings, "MAXIMUM_URL_CHARS", 7)

AVAILABLE_CHARS = ascii_letters + digits


def create_random_code(chars=AVAILABLE_CHARS):
    """
    Creates a random string with the predetermined size
    """
    return "".join(
        [choice(chars) for _ in range(SIZE)]
    )