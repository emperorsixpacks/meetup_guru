import re
from typing import Dict
from urllib.parse import urljoin, urlencode
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

from src.utils.session_manager import Session


class BaseEventScrapper(ABC):
    base_url: str = None
    authentication_url: str = None
    has_authentication: bool = False
    headers: Dict[str, str] = {}

    def __init__(self) -> None:
        self.session = self._create_session()

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "__source_name__"):
            setattr(cls, "__source_name__", cls.__name__)
        if cls.has_authentication and cls.authentication_url is None:
            raise ValueError("Provide a valid authentication url for your source")

    def _create_session(self) -> Session:
        return Session(
            headers=self.headers,
        )

    def authenticate(self):
        pass

    def parse_html(self, html_response, tag):
        soup = BeautifulSoup(html_response, "html.parser")
        soup_result = soup.find_all(tag)
        return soup_result

    def build_url(self, path: str = "", qparams=None):
        url = urljoin(self.base_url, path)
        if qparams:
            query_string = urlencode(qparams)
            url = f"{url}?{query_string}"

        return url

    @abstractmethod
    def scrape(self, path: str = None, qparams: Dict[str, str] = None):
        pass

    @abstractmethod
    def __build_search_url(self):
        pass
