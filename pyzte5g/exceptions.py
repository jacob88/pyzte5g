class AuthFailure(Exception):
    """ Session authentication failure. """

class AccessError(AuthFailure):
    """
        Attempt to access a private value from the ZTE modem API
        while session is not currently authenticated.
    """
