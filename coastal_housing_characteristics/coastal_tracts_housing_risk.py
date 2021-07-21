"""
coastal_tracts_housing_risk.py

Example script for retrieving American Community Survey data for coastal census tracts to 
assess potential building risk
"""
import json
import os
import pandas as pd
import requests
from datetime import datetime

api_token = os.environ["IGGY_API_TOKEN"]


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


def df_to_geojson(df, properties, lon="longitude", lat="latitude"):
    geojson = {"type": "FeatureCollection", "features": []}
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": []},
        }
        feature["geometry"]["coordinates"] = [row[lon], row[lat]]
        for prop in properties:
            feature["properties"][prop] = row[prop]
        geojson["features"].append(feature)
    return geojson


def main():
    # this input file generated by running sql in `coastal_tracts.sql` on Google BigQuery
    tracts_geom = json.load(open("coastal_tracts.json", "r"))
    dataset_id = "acs_census_tract_housing"

    ignore_states = ["78"]  # USVI

    for tract in tracts_geom:
        if tract["state_fips_code"] in ignore_states:
            continue
        try:
            data = get_properties_at_point(
                tract["point_longitude"], tract["point_latitude"], dataset_id
            )
            tract["pct_housing_units_10_or_more_in_structure"] = (
                data[0]["properties"]["pct_housing_units_10_to_19_in_structure"]
                + data[0]["properties"]["pct_housing_units_20_to_49_in_structure"]
                + data[0]["properties"]["pct_housing_units_50_or_more_in_structure"]
            )
            tract["median_structure_age"] = datetime.now().year - data[0][
                "properties"
            ].get("median_year_structure_built")
            tract["housing_units_total"] = data[0]["properties"].get(
                "housing_units_total"
            )
        except (TypeError, IndexError) as e:
            if not tract.get("pct_housing_units_10_or_more_in_structure"):
                tract["pct_housing_units_10_or_more_in_structure"] = None
            if not tract.get("median_structure_age"):
                tract["median_structure_age"] = None
            if not tract.get("housing_units_total"):
                tract["housing_units_total"] = None

    df = pd.DataFrame(tracts_geom)
    df = df.dropna()

    df[
        "percentile:pct_housing_units_10_or_more_in_structure"
    ] = df.pct_housing_units_10_or_more_in_structure.rank(pct=True)
    df["percentile:median_structure_age"] = df.median_structure_age.rank(pct=True)
    df["percentile:housing_units_total"] = df.housing_units_total.rank(pct=True)
    df["risk_percentile_sum"] = (
        df["percentile:pct_housing_units_10_or_more_in_structure"]
        + df["percentile:median_structure_age"]
    )

    geojson = df_to_geojson(df, df.columns, lon="point_longitude", lat="point_latitude")
    with open("coastal_tracts_output.json", "w") as f:
        json.dump(geojson, f, indent=2)


if __name__ == "__main__":
    main()