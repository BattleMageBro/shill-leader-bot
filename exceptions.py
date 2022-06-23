class ServiceError(Exception):
    def __init__(self, **kwargs):
        self.user_message = kwargs.get('user_message')
        self.developer_message = kwargs.get('developer_message')
        super(ServiceError, self).__init__()


class UserError(ServiceError):
    pass