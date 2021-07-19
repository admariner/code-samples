import os
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


def get_properties_at_point(longitude, latitude, dataset_id):
    """
    Given an input longitude/latitude and dataset identifier, retrieve properties
    for features that intersect that point
    """
    url = f"https://api.askiggy.com/properties/v1/datasets/{dataset_id}/select/point"
    headers = {
        "Accept": "application/json",
        "X-Iggy-Token": api_token,
    }
    payload = {"longitude": longitude, "latitude": latitude}
    result = requests.get(url, params=payload, headers=headers).json()
    try:
        data = result["data"]
    except KeyError as e:
        print(f"ERROR: {result['detail']}")
        raise e
    return data


def get_properties_at_buffered_point(longitude, latitude, dataset_id, radius_meters):
    """
    Given an input longitude/latitude and dataset identifier, retrieve properties
    for features that fall within `radius_meters` of that point
    """
    url = f"https://api.askiggy.com/properties/v1/datasets/{dataset_id}/select/buffered-point"
    headers = {
        "Accept": "application/json",
        "X-Iggy-Token": api_token,
    }
    payload = {"longitude": longitude, "latitude": latitude, "radius": radius_meters}
    result = requests.get(url, params=payload, headers=headers).json()
    try:
        data = result["data"]
    except KeyError as e:
        print(f"ERROR: {result['detail']}")
        raise e
    return data

def get_nearest_properties(longitude, latitude, dataset_id, radius_meters):
    """
    Given an input longitude/latitude and dataset identifier, retrieve properties
    for the nearest feature that falls within `radius_meters` of that point
    """
    url = f"https://api.askiggy.com/properties/nearest/v1/datasets/{dataset_id}/select/buffered-point"
    headers = {
        "Accept": "application/json",
        "X-Iggy-Token": api_token,
    }
    payload = {"longitude": longitude, "latitude": latitude, "radius": radius_meters}
    result = requests.get(url, params=payload, headers=headers).json()
    try:
        data = result["data"]
    except KeyError as e:
        print(f"ERROR: {result['detail']}")
        raise e
    return data

