import matplotlib
#matplotlib.use('Agg')
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import ticker
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import numpy as np
from pylab import *
# Important to download matlab files
import scipy.io
from numpy import linspace
from numpy import meshgrid
import numpy.ma as madd
from scipy import signal

import netCDF4
from netCDF4 import Dataset

#%matplotlib inline

import codes as codes
from codes import *

# Analysis in the North and South Hemisphere (Boxes 1,3 (DC) and 2,4 (Sc))

# The first analysis is by considering the whole boxes (correspondent to subdomain 1)

path = '/work/bb1131/b380873/Cumulo/SubDomains_NPY/'

# North Hemisphere

# Import the time series in box 1
box_DC_N = np.load(path+'signals_Box_DC_N_1.npy')[0]
# Import the time series in box 1
box_Sc_N = np.load(path+'signals_Box_Sc_N_1.npy')[0]
# Import the time series in box 3
box_CU_N = np.load(path+'signals_Box_CU_N_1.npy')[0]

# South Hemisphere

# Import the time series in box 1
box_DC_S = np.load(path+'signals_Box_DC_S_1.npy')[0]
# Import the time series in box 1
box_Sc_S = np.load(path+'signals_Box_Sc_S_1.npy')[0]
# Import the time series in box 3
box_CU_S = np.load(path+'signals_Box_CU_S_1.npy')[0]

# Remove the seasonal cycle
# Remove a linear trend
# Normalize to zero mean and unit variance

# North Hemisphere
box_DC_N_anomalies = codes.normalizer(codes.anomalies(box_DC_N))
box_Sc_N_anomalies = codes.normalizer(codes.anomalies(box_Sc_N))
box_CU_N_anomalies = codes.normalizer(codes.anomalies(box_CU_N))
# South Hemisphere
box_DC_S_anomalies = codes.normalizer(codes.anomalies(box_DC_S))
box_Sc_S_anomalies = codes.normalizer(codes.anomalies(box_Sc_S))
box_CU_S_anomalies = codes.normalizer(codes.anomalies(box_CU_S))

correlation_DC_Sc_NH = laggedCorrelogram(box_DC_N_anomalies,box_Sc_N_anomalies,30)
correlation_DC_Sc_SH = laggedCorrelogram(box_DC_S_anomalies,box_Sc_S_anomalies,30)
correlation_DC_CU_NH = laggedCorrelogram(box_DC_N_anomalies,box_CU_N_anomalies,30)
correlation_DC_CU_SH = laggedCorrelogram(box_DC_S_anomalies,box_CU_S_anomalies,30)

plt.plot(correlation_DC_Sc_NH[:,0],correlation_DC_Sc_NH[:,1],label='DC <---> Sc, NH')
plt.plot(correlation_DC_Sc_SH[:,0],correlation_DC_Sc_SH[:,1],label='DC <---> Sc, SH')
plt.plot(correlation_DC_CU_NH[:,0],correlation_DC_CU_NH[:,1],label='DC <---> CU, NH')
plt.plot(correlation_DC_CU_SH[:,0],correlation_DC_CU_SH[:,1],label='DC <---> CU, SH')
plt.legend()
#plt.savefig('corr_DC_Sc_CU_30.pdf',bbox_inches='tight')
#plt.show()

# Signicance test: nothing significant
print('DC <---> Sc, NH '+str(codes.significantCorr(box_DC_N_anomalies,box_Sc_N_anomalies,30,0.005)))
print('DC <---> Sc, SH '+str(codes.significantCorr(box_DC_S_anomalies,box_Sc_S_anomalies,30,0.005)))
print('DC <---> CU, NH '+str(codes.significantCorr(box_DC_N_anomalies,box_CU_N_anomalies,30,0.005)))
print('DC <---> CU, SH '+str(codes.significantCorr(box_DC_S_anomalies,box_CU_S_anomalies,30,0.005)))

