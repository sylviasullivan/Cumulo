# Author: Sylvia Sullivan
import sys, csv, time
import numpy as np
from datetime import datetime,timedelta
from netCDF4 import Dataset

# Initialize the associated times for the different values.
startdate = datetime(2008,1,1,0,0)
timearr = np.array([startdate + timedelta(days=int(i)) for i in np.arange(366)])

# Initialize the associate lats and lons for the different vlaues.
# Assumed that latitude runs 90 N to 90 S by 0.5 deg.
# Excluding the South Pole (-90).

# Assumed that longitude runs east 0 E -> 180 E, 179 W -> 0 W
# from Prime Meridian through the IDL and back to PM.
# Excluding the PM itself (0).
lats = np.arange(90,-89.5,-0.5)
lons1 = np.arange(0.5,180.1,0.5)
lons2 = np.arange(-179.5,0,0.5)
lons = np.concatenate((lons1,lons2),axis=0)

# Load the data set.
basedir = '/work/bb1131/b380873/Cumulo/'
fi = 'year.npy'
jahr = np.load(fi)

# Create the spatiotemporal dimensions.
profnc = Dataset('year.nc','w',format='NETCDF4')
time = profnc.createDimension('time',timearr.shape[0])
lat = profnc.createDimension('latitude',lats.shape[0])
lon = profnc.createDimension('longitude',lons.shape[0])

# Create variables with appropriate dimensions
day = profnc.createVariable('day',np.int,('time'))
month = profnc.createVariable('month',np.int,('time'))
longitood = profnc.createVariable('longitude',np.float32,('longitude'))
latitood = profnc.createVariable('latitude',np.float32,('latitude'))
class1 = profnc.createVariable('class1',np.float32,('time','latitude','longitude'))
class2 = profnc.createVariable('class2',np.float32,('time','latitude','longitude'))
class3 = profnc.createVariable('class3',np.float32,('time','latitude','longitude'))
class4 = profnc.createVariable('class4',np.float32,('time','latitude','longitude'))
class5 = profnc.createVariable('class5',np.float32,('time','latitude','longitude'))
class6 = profnc.createVariable('class6',np.float32,('time','latitude','longitude'))
class7 = profnc.createVariable('class7',np.float32,('time','latitude','longitude'))
class8 = profnc.createVariable('class8',np.float32,('time','latitude','longitude'))

# Set the values of the variables
latitood[:] = lats
latitood.long_name = "Latitude (N to S)"
latitood.units = "deg N"
longitood[:] = lons
longitood.long_name = "Longitude (E to W)"
longitood.units = "deg E"
day[:] = np.array([i.day for i in timearr])
day.long_name = "Day of the month"
day.units = "Day"
month[:] = np.array([i.month for i in timearr])
month.long_name = "Month of the year"
month.units = "Month"
class1[:,:,:] = jahr[:,0,:,:]
class1.long_name = "Fraction of cloud class 1"
class2[:,:,:] = jahr[:,1,:,:]
class2.long_name = "Fraction of cloud class 2"
class3[:,:,:] = jahr[:,2,:,:]
class3.long_name = "Fraction of cloud class 3"
class4[:,:,:] = jahr[:,3,:,:]
class4.long_name = "Fraction of cloud class 4"
class5[:,:,:] = jahr[:,4,:,:]
class5.long_name = "Fraction of cloud class 5"
class6[:,:,:] = jahr[:,5,:,:]
class6.long_name = "Fraction of cloud class 6"
class7[:,:,:] = jahr[:,6,:,:]
class7.long_name = "Fraction of cloud class 7"
class8[:,:,:] = jahr[:,7,:,:]
class8.long_name = "Fraction of cloud class 8"

# Ensure that these are physcially realistic values (0-1).
print('Mean fraction for cloud classes')
print('Class 1: ' + str(np.nanmean(class1)))
print('Class 2: ' + str(np.nanmean(class2)))
print('Class 3: ' + str(np.nanmean(class3)))
print('Class 4: ' + str(np.nanmean(class4)))
print('Class 5: ' + str(np.nanmean(class5)))
print('Class 6: ' + str(np.nanmean(class6)))
print('Class 7: ' + str(np.nanmean(class7)))
print('Class 8: ' + str(np.nanmean(class8)))

# Close the nc file.
profnc.close()

