import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import requests
import shapely.geometry
import json
from shapely.geometry import shape

IGGY_KEY = os.environ["IGGY_API_TOKEN"]

def shapely2geojson(shapely_obj):
    geojson_str = json.dumps(shapely.geometry.mapping(shapely_obj))

    geojson = json.loads(geojson_str)
    geojson["features"][0]["geometry"]["type"] = "Polygon"
    geojson["features"][0]["geometry"]["coordinates"] = geojson["features"][0][
        "geometry"
    ]["coordinates"][0]
    geojson_geom = geojson["features"][0]["geometry"]

    return geojson_geom

def get_cbgs(geometry):
    url = "https://api.iggy.cloud/features/v1/datasets/" \
          "acs_census_blockgroup_housing/select/geojson"

    payload = geometry
    headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "X-Iggy-Token": Iggy_Key}

    response = requests.request("POST",
                                url,
                                json = payload,
                                headers = headers)
    return response

def create_map(cbg, parcel, lat, lon, zoom):
    map = pdk.Deck(
        map_provider="mapbox",
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
        },
        layers=[
            pdk.Layer(
                "GeoJsonLayer",
                data=cbg,
                get_position=["lon", "lat"],
                radius=100,
                pickable=False,
                getFillColor=[3, 17, 86, 255],
                opacity=0.5,
            ),
            pdk.Layer(
                "GeoJsonLayer",
                data=parcel,
                get_position=["lon", "lat"],
                pickable=False,
                stroked=True,
                filled=True,
                getLineColor=[218, 41, 28, 255],
                getFillColor=[218, 41, 28, 255],
            ),
        ],
    )
    return map


def main():
    st.title("Thousand Oaks Housing Data Browser")

    parcels_gdf = gpd.read_file("parcels.geojson")
    parcels_gdf["simple_address"] = (
        parcels_gdf["SitusStreetNumber"] + " " + parcels_gdf["SitusStreetName"]
    )

    parcel_sel = st.selectbox(
        label="Select a parcel...", options=parcels_gdf["simple_address"], index=5
    )

    parcel_sel_gdf = parcels_gdf.loc[
        (parcels_gdf["SitusStreetNumber"] == parcel_sel.split(" ", 1)[0])
        & (parcels_gdf["SitusStreetName"] == parcel_sel.split(" ", 1)[1])
    ]

    iggy_response = get_cbgs(shapely2geojson(parcel_sel_gdf["geometry"]))
    iggy_response_json = iggy_response.json()
    iggy_cbgs = iggy_response_json["data"]
    iggy_cbgs_df = pd.DataFrame(iggy_cbgs)
    iggy_cbgs_gdf = gpd.GeoDataFrame(iggy_cbgs_df)
    iggy_cbgs_gdf["geometry"] = iggy_cbgs_gdf.apply(
        lambda row: shape(row["geometry"]), axis=1
    )
    props_s = pd.Series(iggy_cbgs_df["properties"].iloc[0])
    props_df = props_s.to_frame().rename(columns={0: "Value"})

    deck_map = create_map(
        iggy_cbgs_gdf,
        parcel_sel_gdf,
        parcel_sel_gdf.centroid.y.iloc[0],
        parcel_sel_gdf.centroid.x.iloc[0],
        14,
    )
    st.pydeck_chart(deck_map)
    st.dataframe(props_df)
    deck_map.update()

if __name__ == "__main__":
    main()
