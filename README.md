# Iggy Code Samples


This repo contains code samples that help you get started with the Iggy API. For more details about the API see the [API reference](https://docs.askiggy.com/v0.2.0/reference)


## Samples

### Points within a Boundary

When you are starting with a point and want to know what boundary it is in or want to know properties about the area its in, using [a point selection](https://docs.askiggy.com/v0.2.0/reference/properties-1#get_properties_for_point_properties_v1_datasets__dataset_id__select_point_get) is best. This looks up the boundary your point is in, and returns the properties of that area.

[In this sample we look up bicycle commute stats for census tracts in San Francisco.](points_in_boundaries/bike_commutes/points_in_boundaries.py)

[In another sample we look up the median age of housing units and percent of multi-unit dwellings for coastal communities in the U.S.](points_in_boundaries/coastal_housing_characteristics/coastal_tracts_housing_risk.py)

### Nearby Features

When you are looking for places or things aka "Features" that are nearby to a location you can use the [buffered point selection](https://docs.askiggy.com/v0.2.0/reference/features-1#get_features_for_buffered_point_features_v1_datasets__dataset_id__select_buffered_point_get). This will return all the Features, including the geometries within the radius from the point that you specify.

[In this sample we find all the fire stations within a 3km radius of Downtown Denver.](get_nearby_features/points_nearby.py)

## Python Environment Setup - Starting from Zero

There are main ways to setup your python environment, this is a helpful guide if you are getting started on MacOS:

First, you'll want to install `pyenv` to manage your Python installations

    brew update
    brew install pyenv

(We assume that you already have brew installed, but [if you don't](https://brew.sh))

After `pyenv` is installed, it will ask you do add something to the end of your `.bash_profile` or `.zshrc` (depending on your shell). Please do so and reload your shell (`source ~/.bash_profile` or `source ~/.zshrc`)

We currently target Python 3.8.5. Install that with `pyenv`:

    pyenv install 3.8.5

You can make Python 3.8.5 your default (the one that `python` invokes) using

    pyenv global 3.8.5

Next, you'll want to install `pipenv`. You can do that through `brew` as well

    brew install pipenv

Then, install the dependencies with

    pipenv install
