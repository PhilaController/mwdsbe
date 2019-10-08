from . import data_dir, registry_date
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import os


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
    registry = gpd.GeoDataFrame(registry, geometry="geometry")

    # Set missing geometries to NaN
    invalid = registry.lat.isnull() | registry.lng.isnull()
    registry.loc[invalid, "geometry"] = np.nan

    # Remove entries where the name is "None" or "Same"
    bad_names = registry["dba_name"].str.lower().isin(["same", "none"])
    registry.loc[bad_names, "dba_name"] = np.nan

    # return
    return registry.rename_axis("registry_id")

