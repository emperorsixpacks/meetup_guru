class BaseSessionException(Exception):
    """
    Base exception class for all prompt exceptions
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class ServerTimeOutError(BaseSessionException):
    def __init__(self, location) -> None:
        """
        Initialize ServerTimeOutError with the provided location.
        
        Args:
            location (str): The location of the server.
        """
        self.message = f"server at {location} did not respond"
        super().__init__(self.message)

class FailedToCreateRedisJobError(BaseSessionException):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)