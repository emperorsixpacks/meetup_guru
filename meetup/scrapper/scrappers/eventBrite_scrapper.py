import re
import json
from typing import Dict, Self, Optional

from meetup.scrapper.scrappers.base import BaseEventScrapper
from meetup.utils.helper_classes import EventBriteEvent
from meetup.utils.helper_functions import formate_time, format_date, get_category_by_id

SERVER_DATA_REGEX = re.compile(r"__SERVER_DATA__\s*=\s*({.*?});", re.DOTALL)


class EventBiteScrapper(BaseEventScrapper):
    # has_authentication = True
    base_url = "https://www.eventbrite.com"

    def __init__(self, country, city, category: Optional[str] = None) -> None:
        self.search_url = self.build_search_url(country, city, category)
        self.search_qpararms: Dict[str, str] = {}
        self.total_pages = 0
        super().__init__()

    def __return_server_data(self, path: str = None, qparams: Dict[str, str] = None):
        new_url = self.build_url(path, qparams)
        response = self.session.get(new_url).text
        parsed_html = self.parse_html(response, "script")[11].string
        soup_result = re.search(SERVER_DATA_REGEX, parsed_html).group(1)
        json_data = json.loads(soup_result)

        return json_data

    def search(self, qparams: Dict[str, str] = {}) -> Self:

        json_data = self.__return_server_data(self.search_url, qparams)
        self.total_pages = json_data["search_data"]["events"]["pagination"][
            "page_count"
        ]
        self.search_qpararms = qparams
        return self

    def build_search_url(self, country, city, category_id: Optional[str] = None) -> str:

        return (
            self.build_url(f"d/{country.lower()}--{city.lower()}/all-events/")
            if category_id is None
            else self.build_url(
                f"d/{country.lower()}--{city.lower()}/{get_category_by_id(category_id=category_id)}--events/"
            )
        )

    def return_sub_categories(self):
        pass

    def scrape(self, page_number: int = 1) -> list[EventBriteEvent]:
        if page_number > self.total_pages or page_number < 1:
            raise ValueError("Invalid page number")
        path = self.search_url
        self.search_qpararms["page"] = page_number
        response = self.__return_server_data(path, self.search_qpararms)
        json_data = response["search_data"]["events"]["results"]

        return (
            [
                EventBriteEvent(
                    name=event.get("name"),
                    url=event.get("url"),
                    city=event["primary_venue"]["address"]["city"],
                    country=event["primary_venue"]["address"]["country"],
                    summary=event["summary"],
                    # address=event["address"],
                    image_url=event.get("image")["url"] if event.get("image") else None,
                    is_online_event=event["is_online_event"],
                    start_time=formate_time(event["start_time"]),
                    start_date=format_date(event["start_date"]),
                    end_time=formate_time(event["end_time"]),
                    end_date=format_date(event["end_date"]),
                )
                for event in json_data
            ],
        )



print(EventBiteScrapper("NIgeria", "Lagos").search().scrape())