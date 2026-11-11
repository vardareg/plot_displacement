# Plot Displacement
This repository contains a Python script that processes and visualizes displacement data resulting from earthquakes or other geophysical events. The plot_displacement function generates four different plots to help you better understand the spatial distribution of displacement and its impact on the region of interest.

# Overview

The plot_displacement function is designed to process and visualize displacement data from a time series file, along with other geospatial data such as a digital elevation model (DEM) and fault lines from a shapefile. The function generates four different plots:
    A preview plot of the masked displacement data (in centimeters) on a 2D grid.
    A cross-section plot of the displacement data along a specified line (A-A').
    A plot of the masked displacement data with the cross-section line (A-A') and its labels.
    A final plot showing the masked displacement data over the DEM background with fault lines from the shapefile, along with the cross-section line (A-A') and its labels.
# Setup
Python 3.11 or newer is required. Dependencies are pinned to the latest releases compatible with Python 3.11 as of November 11, 2026. NumPy 2.5 and Rasterio 1.5 require Python 3.12, so this project uses NumPy 2.4.6 and Rasterio 1.4.4 to retain Python 3.11 support.

In order to setup crete a folder and run these commands in terminal.

    git clone https://github.com/vardareg/plot_displacement.git
    pip install .

Run the plotting compatibility test after installation:

    python -m unittest discover -s tests -v
# Usage
 The plot_displacement function included in this repository provides the following features:
    Reads displacement time series data from an HDF5 file and applies a mask from another HDF5 file.
    Converts the displacement data to a 2D grid with geographical coordinates.
    Generates a preview plot of the masked displacement data (in centimeters) on a 2D grid.
    Plots a cross-section of the displacement data along a specified line (A-A') to visualize the profile of the displacement.
    Creates a plot of the masked displacement data with the cross-section line (A-A') and its labels.
    Generates a final plot that overlays the masked displacement data on a digital elevation model (DEM) background, along with fault lines from a shapefile and the cross-section line (A-A') and its labels.
    
    from displacement_visualization.plot_displacement import plot_displacement
    import datetime
    # Example 
    timeseries_file = 'geo_timeseries_ERA5_demErr.h5'# required
    mask_file = 'geo_maskTempCoh.h5'# required
    dem_file = 'demLat_N37_N40_Lon_E038_E042.tif'# required
    shp_file_path = 'MTA_fay.shp'# required
    earthquake_date = datetime.datetime(2020, 1, 24) # required
    # Cross section parametreters y,x (Latitude,Longtitude)
    start_point = (38.19, 39.04)
    end_point = (38.47, 38.85)
    #Set limit for last plot x,y
    xlim = (38, 42)
    ylim = (37, 40)
    plot_displacement(timeseries_file, mask_file, dem_file, shp_file_path, earthquake_date, start_point, end_point, xlim, ylim)

# Input Parameters

The plot_displacement function takes the following input parameters:

    timeseries_file: Path to the time series file (HDF5 format) containing displacement data.
    mask_file: Path to the mask file (HDF5 format) containing a mask to be applied to the displacement data.
    dem_file: Path to the digital elevation model (DEM) file (GeoTIFF format) for the study area.
    shp_file_path: Path to the shapefile containing fault lines to be plotted.
    earthquake_date: Date of the earthquake event as a datetime.date object.
    start_point: Latitude and longitude of the start point (A) of the cross-section line as a tuple (float, float).
    end_point: Latitude and longitude of the end point (A') of the cross-section line as a tuple (float, float).
    xlim: (Optional) Limits for the x-axis (longitude) in the final plot as a tuple (float, float). Default is None.
    ylim: (Optional) Limits for the y-axis (latitude) in the final plot as a tuple (float, float). Default is None.


