import asyncio
import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional, Self
from urllib.parse import urlencode, urljoin

from meetup.scrapper.scrappers.base import BaseEventScrapper
from meetup.utils.global_settings import EventBriteSettings
from meetup.utils.helper_classes import EventBriteEvent
from meetup.utils.helper_functions import (extract_url_parts, format_date,
                                           formate_time, get_category_by_id,
                                           parse_html)
from meetup.utils.session_manager import Session

SERVER_DATA_REGEX = re.compile(r"__SERVER_DATA__\s*=\s*({.*?});", re.DOTALL)
event_brite_settings = EventBriteSettings()
BASE_URL = "https://www.eventbrite.com"


@dataclass
class BaseEventBiteScrapper(BaseEventScrapper):
    base_url = BASE_URL
    country: Optional[str]
    city: Optional[str]
    category: Optional[str]
    session: Session
    # look into fixing the check to make sure an authentication url is passed

    def __post__init__(self) -> None:
        self.search_url = self.build_search_url()
        self.total_pages = 0

    def __return_server_data(
            self,
            path: str = None,
            qparams: Dict[str, str] = None):
        new_url = self.build_url(path, qparams)
        response = self.session.get(new_url).text
        parsed_html = parse_html(response, "script")[11].string
        soup_result = re.search(SERVER_DATA_REGEX, parsed_html).group(1)
        json_data = json.loads(soup_result)

        return json_data

        async def __areturn_server_data(
            self, path: str = None, qparams: Dict[str, str] = None
        ):
            new_url = self.build_url(path, qparams)
            response = await self.session.aget(new_url)
            text = response.text
            parsed_html = await asyncio.to_thread(self.parse_html, text, "script")
            script_tags = parsed_html[11].string
            soup_result = re.search(SERVER_DATA_REGEX, script_tags).group(1)
            json_data = json.loads(soup_result)

            return json_data

        def __search(self, qparams: Dict[str, str] = None) -> Self:
            # TODO this could be made better, we could check if the country or city has been passed
            if qparams is None:
                qparams = {}

            json_data = self.__return_server_data(self.search_url, qparams)
            self.total_pages = json_data["search_data"]["events"]["pagination"][
                "page_count"
            ]
            self.search_qpararms = qparams
            return self

        def __scrape(self, page_number: int = 1) -> list[EventBriteEvent]:
            if not self.check_valid_page_number(page_number):
                return None
            path = self.construct_scrape_url(page_number=page_number)
            response = self.__return_server_data(path, self.search_qpararms)
            json_data = response["search_data"]["events"]["results"]
            return self.create_new_event(json_data=json_data)

        async def __ascrape(self, page_number: int = 1) -> list[EventBriteEvent]:
            if not self.check_valid_page_number(page_number):
                return None
            path = self.construct_scrape_url(page_number=page_number)
            response = await self.__areturn_server_data(path, self.search_qpararms)
            json_data = response["search_data"]["events"]["results"]
            return self.create_new_event(json_data=json_data)

        def check_valid_page_number(self, page_number):
            if page_number > self.total_pages or page_number < 1:
                return False
            return True

        @staticmethod
        def create_new_event(json_data: Dict[str, Any]):

            return [
                EventBriteEvent(
                    name=event.get("name"),
                    url=event.get("url"),
                    city=event["primary_venue"]["address"]["city"],
                    country=event["primary_venue"]["address"]["country"],
                    summary=event["summary"],
                    # address=event["address"],
                    image_url=event.get("image")["url"] if event.get(
                        "image") else None,
                    is_online_event=event["is_online_event"],
                    start_time=formate_time(event["start_time"]),
                    start_date=format_date(event["start_date"]),
                    end_time=formate_time(event["end_time"]),
                    end_date=format_date(event["end_date"]),
                )
                for event in json_data
            ]

        def build_url(self, path: str = None, qparams=None):
            if path is None:
                path = ""

            url = urljoin(self.base_url, path)
            if qparams:
                query_string = urlencode(qparams)
                url = f"{url}?{query_string}"

            return url

        def build_search_url(self, country, city, category_id: Optional[str] = None) -> str:

            return (
                self.build_url(
                    f"d/{country.lower()}--{city.lower()}/all--events/")
                if category_id is None
                else self.build_url(
                    f"d/{country.lower()}--{city.lower()}/{get_category_by_id(
                        category_id=category_id).name.lower()}--events/",
                    qparams={"page": 1},
                )
            )

        def return_sub_categories(self):
            pass  # yet to implement, I do not even know what it is supposed to do sef

        def construct_scrape_url(self, page_number):
            url = extract_url_parts(self.search_url)
            url.qparams["page"] = page_number
            return url.construct_url()


class EventBiteScrapper(BaseEventBiteScrapper):
    def scrape(self): ...
    def search(self, qparams: Dict[str, str] = None): ...
    async def ascrape(self): ...
# TODO: collect longitude and latitude info
