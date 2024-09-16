import re
import json
from typing import Dict

from scrapper.base import BaseEventScrapper
from src.utils.helper_classes import EventBriteEvent, Pagination
from src.utils.helper_functions import formate_time, format_date

SERVER_DATA_REGEX = re.compile(r"__SERVER_DATA__\s*=\s*({.*?});", re.DOTALL)


class EventBiteScrapper(BaseEventScrapper):
    base_url = "https://www.eventbrite.com"

    def scrape(self, path: str = None, qparams: Dict[str, str] = None):
        new_url = self.build_url(path, qparams)
        response = self.session.get(new_url).text

        parsed_html = self.parse_html(response, "script")[11].string
        soup_result = re.search(SERVER_DATA_REGEX, parsed_html).group(1)
        json_data = json.loads(soup_result)

        return Pagination(
            page=json_data["search_data"]["events"]["pagination"]["page_number"],
            total_pages=json_data["search_data"]["events"]["pagination"]["page_count"],
            events=[
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

