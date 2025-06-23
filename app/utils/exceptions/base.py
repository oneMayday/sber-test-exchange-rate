class BaseCustomException(Exception):
    """Шаблон для кастомных ошибок."""
    default_message: str = None

    def __init__(self, message: str = None, status: int = None):
        if message is None:
            message = self.default_message

        self.message = message

        super(BaseCustomException, self).__init__(self.message)
