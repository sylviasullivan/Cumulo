# Author: Sylvia Sullivan
import sys
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
# Important to download matlab files
import scipy.io
from numpy import linspace
from numpy import meshgrid
import numpy.ma as madd
from scipy import signal

import netCDF4
from netCDF4 import Dataset

#%matplotlib inline

# >> sylvia, Use the numerical tools generalized for more dimensions.
import numerical_tools_multid as num
# << sylvia
from num import *

# Analysis in the North and South Hemisphere (Boxes 1,3 (DC) and 2,4 (Sc))
# The first analysis is by considering the whole boxes (correspondent to subdomain 1)

# >> sylvia, Set this directory as necessary
path = '/work/bb1131/b380873/Cumulo/SubDomains_NPY/'
# >> sylvia, Specify the lag, partition, and how many subdomains exist in that partition
lag = 30
partition = 4
cut = 4 # I think it should actually be 64

# North Hemisphere
# Import the time series in box <partition>
# >> sylvia, Remove the [0] index to read all boxes.
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
print('box_DC_N_anomalies shape: ' + str(box_DC_N_anomalies.shape))
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
# Signicance test: set the p-value and return all significant correlations (a = True)
p = 0.01
a = True
# SH iterator map, not sure how to do this better at the moment
iSH = [1, 0, 3, 2]

fig = plt.figure(figsize=(10,8.5)) #9,7.5))
# i is the subdomain from which we take DC, j is the subdomain from which we take Sc/Cu
for i in np.arange(cut):
    for j in np.arange(cut):
        corr_DC_Sc_NH[c] = laggedCorrelogram(box_DC_N_anomalies[i,:],box_Sc_N_anomalies[j,:],lag)
        corr_DC_CU_NH[c] = laggedCorrelogram(box_DC_N_anomalies[i,:],box_CU_N_anomalies[j,:],lag)
        
        corr_DC_Sc_SH[c] = laggedCorrelogram(box_DC_S_anomalies[iSH[i],:],box_Sc_S_anomalies[iSH[j],:],lag)
        corr_DC_CU_SH[c] = laggedCorrelogram(box_DC_S_anomalies[iSH[i],:],box_CU_S_anomalies[iSH[j],:],lag)

        plt.subplot2grid((cut,cut),(i,j))
        plt.plot(corr_DC_Sc_NH[c,:,0],corr_DC_Sc_NH[c,:,1],label='DC <---> Sc, NH')
        plt.plot(corr_DC_Sc_SH[c,:,0],corr_DC_Sc_SH[c,:,1],label='DC <---> Sc, SH')
        plt.plot(corr_DC_CU_NH[c,:,0],corr_DC_CU_NH[c,:,1],label='DC <---> CU, NH')
        plt.plot(corr_DC_CU_SH[c,:,0],corr_DC_CU_SH[c,:,1],label='DC <---> CU, SH')
        plt.ylim([-0.5,0.4])
        plt.title('Box ' + str(i+1) + ' to Box ' + str(j+1))
        c = c + 1

        sig_DC_Sc_NH = num.significantCorr(box_DC_N_anomalies[i,:],box_Sc_N_anomalies[j,:],30,p,a)
        sig_DC_Sc_SH = num.significantCorr(box_DC_S_anomalies[i,:],box_Sc_S_anomalies[j,:],30,p,a)
        sig_DC_Cu_NH = num.significantCorr(box_DC_N_anomalies[i,:],box_CU_N_anomalies[j,:],30,p,a)
        sig_DC_Cu_SH = num.significantCorr(box_DC_S_anomalies[i,:],box_CU_S_anomalies[j,:],30,p,a)
 
        print('Box ' + str(i+1) + ' to Box ' + str(j+1) + ' Iteration ' + str(c))
        print('DC <---> Sc, NH significant at lag(s) '+str(sig_DC_Sc_NH[:,0]) + ' with value(s) ' + str(sig_DC_Sc_NH[:,1]))
        print('DC <---> Sc, SH significant at lag(s) '+str(sig_DC_Sc_SH[:,0]) + ' with value(s) ' + str(sig_DC_Sc_SH[:,1]))
        print('DC <---> CU, NH significant at lag(s) '+str(sig_DC_Cu_NH[:,0]) + ' with value(s) ' + str(sig_DC_Cu_NH[:,1]))
        print('DC <---> CU, SH significant at lag(s) '+str(sig_DC_Cu_SH[:,0]) + ' with value(s) ' + str(sig_DC_Cu_SH[:,1]))

        # Iterate through the significant lags and shade them on the existing plot.
        for elem in sig_DC_Sc_NH[:,0]:
            plt.axvspan(elem-0.5,elem+0.5,ymin=-1,ymax=1,color='blue',alpha=0.3)
        for elem in sig_DC_Sc_SH[:,0]:
            plt.axvspan(elem-0.5,elem+0.5,ymin=-1,ymax=1,color='gold',alpha=0.3)
        for elem in sig_DC_Cu_NH[:,0]:
            plt.axvspan(elem-0.5,elem+0.5,ymin=-1,ymax=1,color='green',alpha=0.3)
        for elem in sig_DC_Cu_SH[:,0]:
            plt.axvspan(elem-0.5,elem+0.5,ymin=-1,ymax=1,color='red',alpha=0.3)
        
#plt.legend()
fig.savefig('corr_sig_DC_Sc_Cu_30[partition' + str(partition) + ']_p' + str(p) + '.pdf',bbox_inches='tight')
plt.show()
