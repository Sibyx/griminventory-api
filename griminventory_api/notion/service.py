import requests
from typing import Dict, Any
from griminventory_api.config import NOTION_API_TOKEN

NOTION_API_URL = "https://api.notion.com"


def get_notion_page_data(item_uuid: str) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {NOTION_API_TOKEN}", "Notion-Version": "2022-06-28"}
    response = requests.get(f"{NOTION_API_URL}/v1/pages/{item_uuid}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch Notion page data: {response.status_code}")
