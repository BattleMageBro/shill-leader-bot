from logg import log


class ServiceError(Exception):
    def __init__(self, **kwargs):
        self.user_message = kwargs.get('user_message')
        self.dev_message = kwargs.get('dev_message')
        super(ServiceError, self).__init__()


class ErrorToCustom(ServiceError):
    def __init__(self, exc, **kwargs):
        self.user_message = 'Unhandled error. Please try again later or contact support.'
        self.dev_message = f'Error. User: {kwargs.get("user")}. Caught {exc.__class__.__name__} with message: {exc.args[0]}'


class UserError(ServiceError):
    pass


class ChatError(ServiceError):
    pass


def to_custom_exc(exc:Exception, user_id:str):
    if not isinstance(exc, ServiceError):
        exc = ErrorToCustom(exc, user=user_id)
    return exc
