"""
Author: Sylvia Sullivan
Reads in the npy dataset and filters the tropics by hemisphere. Adjust the filename read in as <jahr> and the indices in the line thereafter for the hemisphere (line 9) as necessary.

Then the function latlonCut takes <plat> and <plon> as the number of latitudinal and longitudinal subdomains into which you want to decompose and <lbl> as the prefix for the subdomain. For example, the first decomposition splits the longitudes into 2 intervals so that <plat> = 1, <plon> = 2, and <lbl> = 1. The seventh (and last) decomposition splits the longitudes into 64 intervals and latitudes into 4 intervals, so that <plat> = 4, <plon> = 64, and <lbl> = 7.

The time series are averaged over each of the subdomains in this decomposition and stored in a dataframe as the column <lbl><subdomain number>. At the end, the entire dataframe is saved to a pkl named only with <lbl>. So, for example, Subdomains_1.pkl has columns named Subdomain_11 and Subdomain_12. Subdomains_2.pkl has columns named Subdomain_21..Subdomain_24.

"""

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
