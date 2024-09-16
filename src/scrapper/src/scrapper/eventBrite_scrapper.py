import re
import json
from typing import Dict
from scrapper.base import BaseEventScrapper

SERVER_DATA_REGEX = re.compile(r'__SERVER_DATA__\s*=\s*({.*?});', re.DOTALL)

class EventBiteScrapper(BaseEventScrapper):
    base_url = "https://www.eventbrite.com"

    def scrape(self, path: str = None, qparams: Dict[str, str] = None):
        new_url = self.build_url(path, qparams)
        response = self.session.get(new_url).text

        parsed_html = self.parse_html(response, "script")[11].text
        print(parsed_html)

print("hello")
    