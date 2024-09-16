import requests
import re
from scrapper.base import BaseEventScrapper

class EventBiteScrapper(BaseEventScrapper):
    has_authentication = False
    def scrape(self):
        html_response = requests.get(self.authenticate_url).text
        