from abc import ABC, abstractmethod

class BaseEventScrapper(ABC):
    authenticate_url: str = None
    has_authentication: bool = True
    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "__source_name__"):
            setattr(cls, "__source_name__", cls.__name__)
        if hasattr(cls, "has_authentication") and getattr(cls, "has_authentication_url") is None:
            raise ValueError("Provide a valid authentication url for your source")
    
    def authenticate(self):
        pass

    @abstractmethod
    def scrape(self):
        pass
    
    
    