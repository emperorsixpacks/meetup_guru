import json
import requests

from src.utils.global_settings import EventBriteSettings
from src.utils.helper_classes import EventBriteCategory

settings = EventBriteSettings()

header = {
    "Authorization": f"Bearer {settings.eventbrite_private_key}"
}

url = "https://www.eventbriteapi.com/v3/categories/"

response = requests.get(url, headers=header, timeout=60)

with open("extras/eventbrite_categories.json", "w", encoding="utf-8") as f:
    categories = response.json()["categories"]
    json.dump(
        [EventBriteCategory(**category).model_dump() for category in categories], f, indent=4
    )
    