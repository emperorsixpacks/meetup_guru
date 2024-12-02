from functools import partial
from typing import Dict


class BaseEventScrapper(partial):
    base_url: str = None
    authentication_url: str = None

    has_authentication: bool = False
    headers: Dict[str, str] = None

    async def ascrape(self): ...
    def scrape(self): ...

    def search(self): ...
