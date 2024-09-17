import json
import requests

from meetup.utils.global_settings import EventBriteSettings
from meetup.utils.helper_classes import EventBriteCategory
from meetup.utils.helper_functions import return_eventbrite_categories_path

settings = EventBriteSettings()

header = {
    "Authorization": f"Bearer {settings.eventbrite_private_key}"
}

url = "https://www.eventbriteapi.com/v3/categories/"

response = requests.get(url, headers=header, timeout=60)

with open(return_eventbrite_categories_path(), "w", encoding="utf-8") as f:
    categories = response.json()["categories"]
    json.dump(
        [EventBriteCategory(**category).model_dump() for category in categories], f, indent=4
    )
    