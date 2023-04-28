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
