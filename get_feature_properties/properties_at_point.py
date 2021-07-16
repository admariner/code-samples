import os
import json
import requests

api_token = os.environ["IGGY_API_TOKEN"]


def get_properties_intersecting_polygon(geom, dataset_id):
    """
    Given an input geometry and dataset identifier, retrieve properties
    for features that intersect that geomery
    """
    url = f"https://api.askiggy.com/properties/v1/datasets/{dataset_id}/select/geojson"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Iggy-Token": api_token,
    }
    payload = {
        "coordinates": geom["features"][0]["geometry"]["coordinates"],
        "geometry_type": "Polygon",
    }
    result = requests.post(url, json=payload, headers=headers).json()
    try:
        data = result["data"]
    except KeyError as e:
        print(f"ERROR: {result['detail']}")
        raise e
    return data


def main():

    shape_geojson = json.load(open("beaches.json", "r"))
    dataset_id = "acs_census_tract_housing"

    housing_properties = get_properties_intersecting_polygon(shape_geojson, dataset_id)

    with open("output.json", "w") as f:
        json.dump(housing_properties, f, indent=2)


if __name__ == "__main__":
    main()
