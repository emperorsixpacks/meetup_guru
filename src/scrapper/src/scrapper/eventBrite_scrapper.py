from scrapper.base import BaseEventScrapper

class EventBiteScrapper(BaseEventScrapper):
    has_authentication = False
    def scrape(self):
        return super().scrape()