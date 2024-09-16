import re
import json
from typing import Dict, Self

from scrapper.base import BaseEventScrapper
from src.utils.helper_classes import EventBriteEvent
from src.utils.helper_functions import formate_time, format_date

SERVER_DATA_REGEX = re.compile(r"__SERVER_DATA__\s*=\s*({.*?});", re.DOTALL)


class EventBiteScrapper(BaseEventScrapper):
    base_url = "https://www.eventbrite.com"

    def __init__(self, country, city) -> None:
        self.search_url = self.__build_search_url(country, city)
        self.search_qpararms: Dict[str, str] = None
        self.total_pages = 0
        super().__init__()

    def __return_server_data(self, path: str = None, qparams: Dict[str, str] = None):
        new_url = self.build_url(path, qparams)
        response = self.session.get(new_url).text

        parsed_html = self.parse_html(response, "script")[11].string
        soup_result = re.search(SERVER_DATA_REGEX, parsed_html).group(1)
        json_data = json.loads(soup_result)

        return json_data

    def search(self, path: str = None, qparams: Dict[str, str] = None) -> Self:

        json_data = self.__return_server_data(path, qparams)
        self.total_pages = self.search()["search_data"]["events"]["pagination"][
            "page_count"
        ]
        self.search_qpararms = qparams
        return json_data

    def __build_search_url(self, country, city):

        return self.build_url(f"d/{country.lower()}--{city.lower()}/all-events/")

    def return_page_data(self, page_number: int = 1) -> list[EventBriteEvent]:
        if page_number > self.total_pages or page_number < 1:
            raise ValueError("Invalid page number")
        path = self.search_url
        qparams = self.search_qpararms
        qparams["page"] = page_number
        json_data = self.__return_server_data(path, qparams)
        return (
            [
                EventBriteEvent(
                    name=event.get("name"),
                    url=event.get("url"),
                    city=event["primary_venue"]["address"]["city"],
                    country=event["primary_venue"]["address"]["country"],
                    summary=event["summary"],
                    # address=event["address"],
                    image_url=event.get("image")["url"],
                    is_online_event=event["is_online_event"],
                    start_time=formate_time(event["start_time"]),
                    start_date=format_date(event["start_date"]),
                    end_time=formate_time(event["end_time"]),
                    end_date=format_date(event["end_date"]),
                )
                for event in json_data["search_data"]["events"]["results"]
            ],
        )

    def scrape(self, path: str = None, qparams: Dict[str, str] = None):
        pass
