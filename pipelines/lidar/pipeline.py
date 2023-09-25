import xarray as xr
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from typing import Dict

from tsdat import IngestPipeline, get_start_date_and_time_str, get_filename
from utils import add_colorbar, format_time_xticks


class Lidar(IngestPipeline):
    """--------------------------------------------------------------------------------
    LIDAR INGESTION PIPELINE

    Ingest of Lidar data from an AXYS Technologies buoy stationed off the coast of
    Humboldt, CA.  Adding a comment to test changes.

    --------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # Set initial drive position on wind direction
        drive_position = None

        if "morro" in dataset.attrs["location_id"]:
            drive_position = 180
        if "humboldt" in dataset.attrs["location_id"]:
            drive_position = 90

        if drive_position:
            new_direction = dataset["wind_direction"].data + drive_position
            new_direction[new_direction >= 360] -= 360
            dataset["wind_direction"].data = new_direction
            dataset["wind_direction"].attrs[
                "corrections_applied"
            ] = f"Applied {drive_position} degree calibration factor."

        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area
        return dataset

    # Adding a comment to test build
