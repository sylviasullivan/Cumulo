# Author: Sylvia Sullivan
import pickle
import numpy as np
import pandas as pd
import sys

# Load values (could later be the interpolated dataset).
# Here for the NH tropics (0-20N). 120:180 for SH tropics.
jahr = np.load('year.npy')
jahr = jahr[:,:,180:240,:]
mm = jahr.shape[2]   # lat
ll = jahr.shape[3]   # lon

# This guy takes the number of latitudinal and longitudinal
# cuts you want to make and returns a dataframe with the 
# spatially averaged time series in each subdomains. 
# <lbl> acts as the prefix for the dataframe.
def latlonCut(plat,plon,lbl):
    print('Cutting subdomains set ' + str(lbl))

    # Count over the subdomains to label them.
    c = 1
    #print(c)

    # Initialize a dataframe to store time series.
    df = pd.DataFrame()

    # Divide the domain into <plat> latitudinal intervals.
    latint = int(mm/float(plat))
    latsplit = np.arange(0,mm+1,latint)
    # Check lat subdomains: print(latint,latsplit)
    for k in np.arange(len(latsplit)-1):

        # Divide the domain into <plon> longitudinal intervals.
        lonint = int(ll/float(plon))
        lonsplit = np.arange(0,ll+1,lonint)
        # Check lon subdomains: print(lonint,lonsplit)

        # Iterate over these intervals...
        for j in np.arange(len(lonsplit)-1):
            # .. and calculate the latitude-longitude mean over each ..
            chunk = np.nanmean(np.nanmean(jahr[:,:,latsplit[k]:latsplit[k+1],\
                                                   lonsplit[j]:lonsplit[j+1]],axis=3),axis=2)
            # .. and store this in a dataframe tagged with <p> and interval number.
            df['Subdomain_' + str(lbl) + str(c)] = [chunk]
            c += 1
    return df

df1 = latlonCut(1,2,1); df1.to_pickle('Subdomains_1.pkl')
df2 = latlonCut(1,4,2); df2.to_pickle('Subdomains_2.pkl')
df3 = latlonCut(1,8,3); df3.to_pickle('Subdomains_3.pkl')
df4 = latlonCut(1,16,4); df4.to_pickle('Subdomains_4.pkl')
df5 = latlonCut(2,16,5); df5.to_pickle('Subdomains_5.pkl')
df6 = latlonCut(2,32,6); df6.to_pickle('Subdomains_6.pkl')
df7 = latlonCut(4,64,7); df7.to_pickle('Subdomains_7.pkl')
