import os
import requests

from services.auth_service import get_access_token

BASE_URL = os.getenv("BASE_URL")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")


def fetch_device_readings(device_id, start_time, end_time, resolution, measurement):
    """Handles external API call to fetch device readings."""
    url = f"{BASE_URL}/devices/{device_id}/readings"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Accept": "application/json",
    }
    params = {
        "startTime": start_time,
        "endTime": end_time,
        "resolution": resolution,
        "measurement": measurement,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)
