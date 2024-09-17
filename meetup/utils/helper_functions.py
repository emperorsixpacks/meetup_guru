import os
import json
from datetime import datetime
from meetup.utils.base import return_app_dir


def format_date(input_date: datetime):
    return datetime.strptime(input_date, "%Y-%m-%d").date()


def formate_time(input_time: str):
    return datetime.strptime(input_time, "%H:%M").time()


def return_eventbrite_categories_path():
    return os.path.join(return_app_dir(__file__), "extras/eventbrite_categories.json")


def open_eventbrite_categories_json():
    with open(return_eventbrite_categories_path(), "r", encoding="utf-8") as f:
        return json.loads(f)


def get_category_by_id(category_id: int):
    json_data = open_eventbrite_categories_json()
    return next(
        (category for category in json_data if category["id"] == category_id),
        None,
    )
