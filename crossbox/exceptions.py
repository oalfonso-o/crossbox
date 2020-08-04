from django.core.exceptions import PermissionDenied


class LimitExceed(PermissionDenied):
    """ Raised when a record that is going to be created will exceed
    the limit permited
    """
    pass
