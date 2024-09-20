import os
import json
from uuid import UUID
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from meetup.utils.base import return_app_dir
from meetup.utils.helper_classes import URL


def format_date(input_date: datetime):
    return datetime.strptime(input_date, "%Y-%m-%d").date()


def formate_time(input_time: str):
    return datetime.strptime(input_time, "%H:%M").time()


def return_eventbrite_categories_path():
    return os.path.join(return_app_dir(__file__), "extras/eventbrite_categories.json")


def open_eventbrite_categories_json():
    with open(return_eventbrite_categories_path(), "r", encoding="utf-8") as f:
        return json.load(f)


def get_category_by_id(category_id: int):
    json_data = open_eventbrite_categories_json()
    return next(
        (category for category in json_data if category["id"] == category_id),
        None,
    )


def is_valid_uuid(input_str: str):
    try:
        UUID(input_str)
        return True
    except ValueError:
        return False


def extract_url_parts(url: str) -> URL:
    parsed_url = urlparse(url)

    scheme = parsed_url.scheme
    path = parsed_url.path
    query_params = parse_qs(parsed_url.query)

    return URL(scheme=scheme, path=path, qparams=query_params)


def flatten_events(nested_list, flat_list=[]):
    # Base case: if the input is not a list, return an empty list
    if not isinstance(nested_list, (list, tuple)):
        return []

    try:
        if not isinstance(flat_list[0], list):
            return flat_list
    except IndexError:
        pass

    for item in nested_list:
        if isinstance(item, (list, tuple)):
            flat_list.extend(item)
            continue
        flat_list.append(item, flat_list)

    return flatten_events(nested_list=flat_list)
