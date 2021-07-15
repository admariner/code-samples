import os
import json
import requests
from pprint import pprint

api_token = os.environ["IGGY_API_TOKEN"]


def get_fire_stations(latitude, longitude):
    """
    Given a latitude and longitude query Iggy API for nearby fire stations.
    """
    r = requests.get(
        "https://api.askiggy.com/features/v1/datasets/hifld_fire_stations/select/buffered-point",
        params={"latitude": latitude, "longitude": longitude, "radius": 3000},  # 3km
        headers={"X-Iggy-Token": api_token},
    )

    return r.json()["data"]


def main():

    latitude = 39.753394
    longitude = -104.977853

    stations = get_fire_stations(latitude, longitude)

    for s in stations:
        s['type'] = "Feature"

    print(json.dumps({"type": "FeatureCollection", "features": stations}))

if __name__ == "__main__":
    main()
