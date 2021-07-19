WITH tract_ids AS (
    SELECT DISTINCT tracts.geo_id FROM 
    `bigquery-public-data.geo_census_tracts.us_census_tracts_national` tracts
            JOIN `bigquery-public-data.geo_us_boundaries.coastline` coast
            ON ST_INTERSECTS(
                tracts.tract_geom,
                coast.coastline_geom
            )
        WHERE
            (
                coast.name = 'Atlantic'
                OR coast.name = 'Gulf'
            ) AND tracts.area_land_meters > 0
),
tract_data AS (
    SELECT 
        t1.geo_id,
        t2.state_name,
        t2.state_fips_code,
        t2.county_fips_code,
        t2.tract_ce,
        ST_CENTROID(t2.tract_geom) AS centroid,
        t2.tract_geom AS GEOMETRY
    FROM 
        tract_ids t1
        LEFT JOIN `bigquery-public-data.geo_census_tracts.us_census_tracts_national` t2
        ON t1.geo_id = t2.geo_id
),
tracts_with_names AS (
    SELECT
        generate_uuid() AS id,
        tract_data.*,
        bounds.name AS place_name,
        bounds.placetype
    FROM
        tract_data
        JOIN `bigquery-public-data.geo_whos_on_first.geojson` geo
        ON st_intersects(
            tract_data.geometry,
            geo.geom
        )
        JOIN `bigquery-public-data.geo_whos_on_first.names` bounds
        ON geo.id = bounds.id
    WHERE
        bounds.language = 'eng'
        AND bounds.private_use = 'x_preferred'
        AND (bounds.placetype = 'locality' or bounds.placetype='county')
),
unique_tracts AS (
    SELECT
        *
    EXCEPT(RANK)
    FROM
        (
            SELECT
                *,
                RANK() over (
                    PARTITION BY geo_id
                    ORDER BY
                        placetype DESC,
                        id
                ) AS RANK
            FROM
                tracts_with_names
        )
    WHERE
        RANK = 1
)
SELECT
    geo_id,
    state_name,
    place_name,
    state_fips_code,
    county_fips_code,
    tract_ce,
    st_x(centroid) AS centroid_longitude,
    st_y(centroid) AS centroid_latitude,
    -- geometry
FROM
    unique_tracts;