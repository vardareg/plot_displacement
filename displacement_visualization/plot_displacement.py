import h5py
import numpy as np
import matplotlib.pyplot as plt
import datetime
from geopy.distance import geodesic
import rasterio
from rasterio.plot import show
import geopandas as gpd

def plot_displacement(timeseries_file, mask_file, dem_file, shp_file_path, earthquake_date, start_point, end_point, xlim=None, ylim=None):
    """
Plots masked displacement data, cross-section plot, masked displacement with cross-section line, and masked
displacement over DEM background with fault lines from a shapefile.

Parameters:
-----------
timeseries_file : str
    Path to the time series file (HDF5 format) containing displacement data.
mask_file : str
    Path to the mask file (HDF5 format) containing a mask to be applied to the displacement data.
dem_file : str
    Path to the digital elevation model (DEM) file (GeoTIFF format) for the study area.
shp_file_path : str
    Path to the shapefile containing fault lines to be plotted.
earthquake_date : datetime.date
    Date of the earthquake event.
start_point : tuple (float, float)
    Latitude and longitude of the start point (A) of the cross-section line.
end_point : tuple (float, float)
    Latitude and longitude of the end point (A') of the cross-section line.
xlim : tuple (float, float), optional
    Limits for the x-axis (longitude) in the final plot. Default is None.
ylim : tuple (float, float), optional
    Limits for the y-axis (latitude) in the final plot. Default is None.

Returns:
--------
None

This function generates four plots:
1. A preview plot of the masked displacement data on a 2D grid.
2. A cross-section plot of the displacement data along a specified line (A-A').
3. A plot of the masked displacement data with the cross-section line (A-A') and its labels.
4. A final plot showing the masked displacement data over the DEM background with fault lines from the shapefile,
    along with the cross-section line (A-A') and its labels.
    """
    with h5py.File(timeseries_file, 'r') as f:
        dates = f['date'][:]
        displacement = f['timeseries'][:]
        
        # Get the geospatial information and convert to float
        lon_step = float(f.attrs['X_STEP'])
        lat_step = float(f.attrs['Y_STEP'])
        lon_origin = float(f.attrs['X_FIRST'])
        lat_origin = float(f.attrs['Y_FIRST'])

    # Load the mask file and read the mask data
    with h5py.File(mask_file, 'r') as f:
        mask = f['mask'][:]

    # Apply the mask to the displacement dataset
    displacement_masked = np.where(mask, displacement, np.nan)

    # Convert dates to datetime objects
    dates = [datetime.datetime.strptime(date.decode('utf-8'), '%Y%m%d') for date in dates]
    begin_row = 0
    end_row = displacement.shape[1]
    begin_column = 0
    end_column = displacement.shape[2]

    # Convert row and column indices to latitude and longitude
    begin_lat = lat_origin + begin_row * lat_step
    end_lat = lat_origin + end_row * lat_step
    begin_lon = lon_origin + begin_column * lon_step
    end_lon = lon_origin + end_column * lon_step

    # Extract the masked displacement time series data along the bounding_box
    bounding_box_displacement_masked = displacement_masked[:, begin_row:end_row, begin_column:end_column]

    # Find the indices of the dates immediately before and after the earthquake
    index_before = max(i for i, date in enumerate(dates) if date < earthquake_date)
    index_after = min(i for i, date in enumerate(dates) if date > earthquake_date)

    # Get the dates before and after the earthquake
    date_before = dates[index_before]
    date_after = dates[index_after]

    # Compute the  in displacement between the two dates for the masked data
    displacement__masked = bounding_box_displacement_masked[index_after, :, :] - bounding_box_displacement_masked[index_before, :, :]
    # Prepare the longitude and latitude arrays
    lons = np.arange(begin_lon, end_lon, lon_step)
    lats = np.arange(begin_lat, end_lat, lat_step)

    # Create a figure with 600 DPI
    plt.figure(dpi=600)

    # Convert displacement  to centimeters
    displacement__masked_cm = displacement__masked * 100

    # Calculate the color limits for equal positive and negative range
    vmin = np.nanmin(displacement__masked_cm)
    vmax = np.nanmax(displacement__masked_cm)
    clim = max(abs(vmin), abs(vmax))

    # Preview Plot

    plt.imshow(displacement__masked_cm, cmap='jet', aspect='auto', extent=[begin_lon, end_lon, end_lat, begin_lat], interpolation='bicubic', vmin=-clim, vmax=clim)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar(label='Displacement  (cm)')
    plt.axis('equal')
    plt.show()

    # Convert latitude and longitude to row and column indices
    start_row = int(round((start_point[0] - lat_origin) / lat_step))
    start_col = int(round((start_point[1] - lon_origin) / lon_step))
    end_row = int(round((end_point[0] - lat_origin) / lat_step))
    end_col = int(round((end_point[1] - lon_origin) / lon_step))

    # Extract the displacement data along the cross-section line
    num_points = max(abs(end_row - start_row), abs(end_col - start_col)) + 1
    cross_section_rows = np.linspace(start_row, end_row, num_points, dtype=int)
    cross_section_cols = np.linspace(start_col, end_col, num_points, dtype=int)

    cross_section_displacement = displacement__masked[cross_section_rows, cross_section_cols] *100

    # Calculate the distance between the points along the cross-section line in kilometers
    point_distances = [geodesic((lats[row], lons[col]), (lats[start_row], lons[start_col])).km for row, col in zip(cross_section_rows, cross_section_cols)]

    # Update the cross-section plot x-axis to display distance in kilometers
    plt.figure(dpi=600)
    plt.plot(point_distances, cross_section_displacement, label="A-A'")
    plt.xlabel("Distance along cross-section (km)")
    plt.ylabel("Displacement  (cm)")
    plt.legend()
    plt.show()

    # Add the cross-section line to the first plot
    plt.figure(dpi=600)
    plt.imshow(displacement__masked_cm, cmap='jet', aspect='auto', extent=[begin_lon, end_lon, end_lat, begin_lat], interpolation='bicubic', vmin=-clim, vmax=clim)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar(label='Displacement  (cm)')

    # Plot the cross-section line
    plt.plot([start_point[1], end_point[1]], [start_point[0], end_point[0]], 'k--', linewidth=1, label="A-A'")
    # Add labels "A" and "A'" to the beginning and end points of the cross-section line
    plt.text(start_point[1]+0.05, start_point[0]-0.15, 'A', fontsize=12, color='black', ha='right', va='bottom')
    plt.text(end_point[1], end_point[0], "A'", fontsize=12, color='black', ha='right', va='baseline')
    plt.legend()
    plt.axis('equal')
    plt.show()

    # Read the DEM data
    with rasterio.open(dem_file) as src:
        dem_data = src.read(1, masked=True)
        dem_transform = src.transform

    # Create the figure with the DEM background and the displacement data
    fig, ax = plt.subplots(dpi=600)
    show(dem_data, ax=ax, transform=dem_transform, cmap= "gray", alpha=1)
    plt.imshow(displacement__masked_cm, cmap="jet", aspect='auto', extent=[begin_lon, end_lon, end_lat, begin_lat], interpolation='bicubic', vmin=-clim, vmax=clim, alpha=1)

    shp_file = gpd.read_file(shp_file_path)
    shp_file.plot(ax=plt.gca(), facecolor='none', edgecolor='black', label='Faults',linewidth=0.5)

    plt.legend()# Add labels, title, and colorbar
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar(label='Displacement  (cm)',shrink=0.8)
    #plt.title(f'Displacement for Elaziğ {earthquake_date.year} Earthquake between {date_before.date()} and {date_after.date()}')

    # Plot the cross-section line
    plt.plot([start_point[1], end_point[1]], [start_point[0], end_point[0]], 'k--', linewidth=1, label="A-A'")
    plt.text(start_point[1]+0.05, start_point[0]-0.2, 'A', fontsize=12, color='black', ha='right', va='bottom')
    plt.text(end_point[1], end_point[0], "A'", fontsize=12, color='black', ha='right', va='baseline')
    plt.legend()
    plt.gca().set_aspect('equal')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.show()

# Example 
def example_usage():
    timeseries_file = 'geo_timeseries_ERA5_demErr.h5'
    mask_file = 'geo_maskTempCoh.h5'
    dem_file = 'demLat_N37_N40_Lon_E038_E042.tif'
    shp_file_path = 'MTA_fay.shp'
    earthquake_date = datetime.datetime(2020, 1, 24)
    start_point = (38.19, 39.04)
    end_point = (38.47, 38.85)
    xlim = (38, 42)
    ylim = (37, 40)
    plot_displacement(timeseries_file, mask_file, dem_file, shp_file_path, earthquake_date, start_point, end_point, xlim, ylim)

