# Plot Displacement
This repository contains a Python script that processes and visualizes displacement data resulting from earthquakes or other geophysical events. The plot_displacement function generates four different plots to help you better understand the spatial distribution of displacement and its impact on the region of interest.

# Overview

The plot_displacement function is designed to process and visualize displacement data from a time series file, along with other geospatial data such as a digital elevation model (DEM) and fault lines from a shapefile. The function generates four different plots:

    A preview plot of the masked displacement data (in centimeters) on a 2D grid.
    A cross-section plot of the displacement data along a specified line (A-A').
    A plot of the masked displacement data with the cross-section line (A-A') and its labels.
    A final plot showing the masked displacement data over the DEM background with fault lines from the shapefile, along with the cross-section line (A-A') and its labels.

# Dependencies

The function requires the following Python packages:

    h5py
    numpy
    matplotlib
    datetime
    geopy
    rasterio
    geopandas

Make sure to install these packages before running the plot_displacement function.

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
