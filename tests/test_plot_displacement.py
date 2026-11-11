import datetime
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")

import geopandas as gpd
import h5py
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import LineString

from displacement_visualization.plot_displacement import plot_displacement


class PlotDisplacementTest(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_plots_hdf5_displacement_with_raster_and_fault_overlay(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            timeseries = root / "timeseries.h5"
            mask_file = root / "mask.h5"
            dem_file = root / "dem.tif"
            faults = root / "faults.shp"

            with h5py.File(timeseries, "w") as dataset:
                dataset["date"] = np.array([b"20200101", b"20200103"])
                dataset["timeseries"] = np.stack(
                    [np.zeros((4, 4)), np.full((4, 4), 0.01)]
                )
                dataset.attrs.update(
                    X_FIRST=20.0, Y_FIRST=10.0, X_STEP=1.0, Y_STEP=1.0
                )
            with h5py.File(mask_file, "w") as dataset:
                mask = np.ones((4, 4), dtype=bool)
                mask[3, 3] = False
                dataset["mask"] = mask
            with rasterio.open(
                dem_file, "w", driver="GTiff", width=4, height=4,
                count=1, dtype="float32", crs="EPSG:4326",
                transform=from_origin(20, 14, 1, 1),
            ) as dataset:
                dataset.write(np.ones((4, 4), dtype="float32"), 1)
            gpd.GeoDataFrame(
                geometry=[LineString([(20, 10), (22, 12)])], crs="EPSG:4326"
            ).to_file(faults)

            with patch.object(plt, "show") as show:
                plot_displacement(
                    str(timeseries), str(mask_file), str(dem_file), str(faults),
                    datetime.datetime(2020, 1, 2), (10, 20), (12, 22),
                    xlim=(20, 24), ylim=(10, 14),
                )

            self.assertEqual(show.call_count, 4)
            figures = [plt.figure(number) for number in plt.get_fignums()]
            self.assertEqual(len(figures), 4)
            profile = figures[1].axes[0].lines[0]
            np.testing.assert_allclose(profile.get_ydata(), [1, 1, 1])
            self.assertEqual(profile.get_xdata()[0], 0)
            self.assertTrue(np.all(np.diff(profile.get_xdata()) > 0))
            self.assertTrue(np.ma.getmaskarray(figures[0].axes[0].images[0].get_array())[3, 3])
            self.assertTrue(figures[3].axes[0].collections)
            np.testing.assert_allclose(figures[3].axes[0].get_xlim(), [20, 24])
            np.testing.assert_allclose(figures[3].axes[0].get_ylim(), [10, 14])


if __name__ == "__main__":
    unittest.main()
