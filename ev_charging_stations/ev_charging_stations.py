import json
import os
import requests

api_token = os.getenv("IGGY_API_TOKEN")

dataset = "nrel_ev_stations"
url = f"https://api.askiggy.com/properties/v1/datasets/{dataset}/select/buffered-point"


def get_charging_stations(latitude, longitude):
    response = requests.request(
        "GET",
        url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "radius": 10000,
            "limit": 10,
        },
        headers={"X-Iggy-Token": api_token, "Accept": "application/json"},
    )

    if len(response.json()["data"]) > 0:
        return response.json()["data"]
    else:
        return None


def main():

    locations = [
        {"name": "Frisco, TX", "latitude": 33.143772, "longitude": -96.790743},
        {"name": "Goodyear, AZ", "latitude": 33.432501, "longitude": -112.403174},
        {"name": "Durham, NC", "latitude": 36.014183, "longitude": -78.924521},
    ]

    for i, location in enumerate(locations):
        locations[i]["ev_stations"] = get_charging_stations(
            location["latitude"], location["longitude"]
        )

    with open("ev_charging_stations_output.json", "w") as fout:
        json.dump(locations, fout, indent=2)


if __name__ == "__main__":
    main()
