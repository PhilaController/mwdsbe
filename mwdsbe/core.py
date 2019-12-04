from . import data_dir, registry_date
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import os


def _load_philly_msa():
    """
    Load the boundary file for the Philadelphia MSA
    """
    URL = "https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_cbsa_5m.zip"
    msa = gpd.read_file(URL).query(
        "NAME == 'Philadelphia-Camden-Wilmington, PA-NJ-DE-MD'"
    )

    return msa.to_crs(epsg=4326)


def load_registry():
    """
    Load the geo-coded version of the OEO registry of minority/women/disabled 
    owned businesses. 

    Note
    ----
    Source: https://phila.mwdsbe.com/

    Returns
    -------
    registry : geopandas.GeoDataFrame
        The formatted registry of businesses
    """
    # Load the data
    filename = os.path.join(data_dir, "registry", f"data_{registry_date}_processed.csv")
    registry = pd.read_csv(filename)

    # Convert to a GeoDataFrame
    registry["geometry"] = [Point(i, j) for i, j in zip(registry.lng, registry.lat)]
    registry = gpd.GeoDataFrame(
        registry, geometry="geometry", crs={"init": "epsg:4326"}
    )

    # Set missing geometries to NaN
    invalid = registry.lat.isnull() | registry.lng.isnull()
    registry.loc[invalid, "geometry"] = np.nan

    # Remove entries where the name is "None" or "Same"
    bad_names = registry["dba_name"].str.lower().isin(["same", "none"])
    registry.loc[bad_names, "dba_name"] = np.nan

    # add Philly MSA
    msa = _load_philly_msa()
    matched = gpd.sjoin(
        registry.dropna(subset=["lat"]), msa.to_crs(registry.crs), op="within"
    )

    # Set the index
    registry = registry.set_index("registry_id")

    registry["in_philly_msa"] = False
    registry.loc[matched["registry_id"], "in_philly_msa"] = True

    # return
    return registry

