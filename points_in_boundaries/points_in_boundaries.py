import os
import json
import requests
from pprint import pprint

api_token = os.environ["IGGY_API_TOKEN"]


def get_bike_commutes(latitude, longitude):
    """
    Given a latitude and longitude query Iggy API for how many people commute by bicycle in a census tract.
    """
    r = requests.get(
        "https://api.askiggy.com/properties/v1/datasets/acs_census_tract_commute/select/point",
        params={"latitude": latitude, "longitude": longitude},
        headers={"X-Iggy-Token": api_token},
    )

    if len(r.json()["data"]) > 0:
        return r.json()["data"][0]["properties"]["pop_commutes_by_bicycle"]
    else:
        return None


def main():
    with open("points.json") as f:
        points = json.load(f)

    commutes = []
    for p in points:
        commutes.append(
            (
                p["latitude"],
                p["longitude"],
                get_bike_commutes(p["latitude"], p["longitude"]),
            )
        )

    pprint(commutes)


if __name__ == "__main__":
    main()
