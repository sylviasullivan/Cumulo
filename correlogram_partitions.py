# Author: Sylvia Sullivan
import sys
import matplotlib
#matplotlib.use('Agg')
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import ticker
#from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
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

import numerical_tools_multid as num
from num import *

# Analysis in the North and South Hemisphere (Boxes 1,3 (DC) and 2,4 (Sc))

# The first analysis is by considering the whole boxes (corresponding to subdomain 1)

path = '/work/bb1131/b380873/Cumulo/SubDomains_NPY/'
# Specify the lag you want, which partition, and how many subdomains exist in that partition
lag = 30
partition = 2
cut = 2

# North Hemisphere
# Import the time series in box <partition>
box_DC_N = np.load(path+'signals_Box_DC_N_' + str(partition) + '.npy')
box_Sc_N = np.load(path+'signals_Box_Sc_N_' + str(partition) + '.npy')
box_CU_N = np.load(path+'signals_Box_CU_N_' + str(partition) + '.npy')

# South Hemisphere
# Import the time series in box <partition>
box_DC_S = np.load(path+'signals_Box_DC_S_' + str(partition) + '.npy')
box_Sc_S = np.load(path+'signals_Box_Sc_S_' + str(partition) + '.npy')
box_CU_S = np.load(path+'signals_Box_CU_S_' + str(partition) + '.npy')

# Remove the seasonal cycle
# Remove a linear trend
# Normalize to zero mean and unit variance

# North Hemisphere
box_DC_N_anomalies = num.normalizer(num.anomalies(box_DC_N))
box_Sc_N_anomalies = num.normalizer(num.anomalies(box_Sc_N))
box_CU_N_anomalies = num.normalizer(num.anomalies(box_CU_N))

# South Hemisphere
box_DC_S_anomalies = num.normalizer(num.anomalies(box_DC_S))
box_Sc_S_anomalies = num.normalizer(num.anomalies(box_Sc_S))
box_CU_S_anomalies = num.normalizer(num.anomalies(box_CU_S))

corr_DC_Sc_NH = np.zeros((cut**2,lag*2+1,2))
corr_DC_Sc_SH = np.zeros((cut**2,lag*2+1,2))
corr_DC_CU_NH = np.zeros((cut**2,lag*2+1,2))
corr_DC_CU_SH = np.zeros((cut**2,lag*2+1,2))

c = 0
fs = 10
fig = plt.figure(figsize=(11,13.5))
for i in np.arange(cut):
    for j in np.arange(cut):
        corr_DC_Sc_NH[c] = laggedCorrelogram(box_DC_N_anomalies[i,:],box_Sc_N_anomalies[j,:],lag)
        corr_DC_Sc_SH[c] = laggedCorrelogram(box_DC_S_anomalies[i,:],box_Sc_S_anomalies[j,:],lag)
        corr_DC_CU_NH[c] = laggedCorrelogram(box_DC_N_anomalies[i,:],box_CU_N_anomalies[j,:],lag)
        corr_DC_CU_SH[c] = laggedCorrelogram(box_DC_S_anomalies[i,:],box_CU_S_anomalies[j,:],lag)

        plt.subplot2grid((cut,cut),(i,j))
        plt.plot(corr_DC_Sc_NH[c,:,0],corr_DC_Sc_NH[c,:,1],label='DC <---> Sc, NH')
        plt.plot(corr_DC_Sc_SH[c,:,0],corr_DC_Sc_SH[c,:,1],label='DC <---> Sc, SH')
        plt.plot(corr_DC_CU_NH[c,:,0],corr_DC_CU_NH[c,:,1],label='DC <---> CU, NH')
        plt.plot(corr_DC_CU_SH[c,:,0],corr_DC_CU_SH[c,:,1],label='DC <---> CU, SH')
        plt.ylim([-0.5,0.4])
        plt.title('Box ' + str(i+1) + ' to Box ' + str(j+1))
        c = c + 1

i = 30; j = 31;k = 3
print(corr_DC_Sc_NH[k,i:j,1])
print(corr_DC_Sc_SH[k,i:j,1])
print(corr_DC_CU_NH[k,i:j,1])
print(corr_DC_CU_SH[k,i:j,1])
sys.exit()
plt.legend(fontsize=fs)
#plt.savefig('corr_DC_Sc_CU_' + str(lag) + '[partition' + str(partition) + '].pdf',bbox_inches='tight')
plt.show()
sys.exit()

# Signicance test: nothing significant
print('DC <---> Sc, NH '+str(num.significantCorr(box_DC_N_anomalies,box_Sc_N_anomalies,30,0.005)))
print('DC <---> Sc, SH '+str(num.significantCorr(box_DC_S_anomalies,box_Sc_S_anomalies,30,0.005)))
print('DC <---> CU, NH '+str(num.significantCorr(box_DC_N_anomalies,box_CU_N_anomalies,30,0.005)))
print('DC <---> CU, SH '+str(num.significantCorr(box_DC_S_anomalies,box_CU_S_anomalies,30,0.005)))

