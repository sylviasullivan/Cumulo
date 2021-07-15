# -*- coding: utf-8 -*-
# importing libraries

# Author: Fabrizio Falasca
# Way more libraries that I need here! Sue me if you must.
from scipy import misc
import numpy as np
from pylab import *
import scipy.io
from numpy import linspace
from numpy import meshgrid
import numpy.ma as madd
from scipy import signal
import scipy.stats
import time

# Function to remove the seasonal cycle from
# daily time series
def anomalies(ts):

    # x is a daily time series

    # Remove a trend
    x = signal.detrend(ts)

    # To remove the seasonal cycle we want to remove
    # to each day in month X the average value in month X

    ############# January #############
    first_day_Jan = 0
    last_day_Jan = 31
    jan_mean = np.nanmean(x[first_day_Jan:last_day_Jan])
    ############# February #############
    first_day_Feb = last_day_Jan
    last_day_Feb = last_day_Jan + 29
    feb_mean = np.nanmean(x[first_day_Feb:last_day_Feb])
    ############# March #############
    first_day_Mar = last_day_Feb
    last_day_Mar = last_day_Feb + 31
    mar_mean = np.nanmean(x[first_day_Mar:last_day_Mar])
    ############# April #############
    first_day_Apr = last_day_Mar
    last_day_Apr = last_day_Mar + 30
    apr_mean = np.nanmean(x[first_day_Apr:last_day_Apr])
    ############# May #############
    first_day_May = last_day_Apr
    last_day_May = last_day_Apr + 31
    may_mean = np.nanmean(x[first_day_May:last_day_May])
    ############# June #############
    first_day_Jun = last_day_May
    last_day_Jun = last_day_May + 30
    jun_mean = np.nanmean(x[first_day_Jun:last_day_Jun])
    ############# July #############
    first_day_Jul = last_day_Jun
    last_day_Jul = last_day_Jun + 31
    jul_mean = np.nanmean(x[first_day_Jul:last_day_Jul])
    ############# August #############
    first_day_Aug = last_day_Jul
    last_day_Aug = last_day_Jul + 31
    aug_mean = np.nanmean(x[first_day_Aug:last_day_Aug])
    ############# September #############
    first_day_Sep = last_day_Aug
    last_day_Sep = last_day_Aug + 30
    sep_mean = np.nanmean(x[first_day_Sep:last_day_Sep])
    ############# October #############
    first_day_Oct = last_day_Sep
    last_day_Oct = last_day_Sep + 31
    oct_mean = np.nanmean(x[first_day_Oct:last_day_Oct])
    ############# November #############
    first_day_Nov = last_day_Oct
    last_day_Nov = last_day_Oct + 30
    nov_mean = np.nanmean(x[first_day_Nov:last_day_Nov])
    ############# December #############
    first_day_Dec = last_day_Nov
    last_day_Dec = last_day_Nov + 31
    dec_mean = np.nanmean(x[first_day_Dec:last_day_Dec])

    # Remove the mean
    x_Jan = x[first_day_Jan:last_day_Jan] - jan_mean
    x_Feb = x[first_day_Feb:last_day_Feb] - feb_mean
    x_Mar = x[first_day_Mar:last_day_Mar] - mar_mean
    x_Apr = x[first_day_Apr:last_day_Apr] - apr_mean
    x_May = x[first_day_May:last_day_May] - may_mean
    x_Jun = x[first_day_Jun:last_day_Jun] - jun_mean
    x_Jul = x[first_day_Jul:last_day_Jul] - jul_mean
    x_Aug = x[first_day_Aug:last_day_Aug] - aug_mean
    x_Sep = x[first_day_Sep:last_day_Sep] - sep_mean
    x_Oct = x[first_day_Oct:last_day_Oct] - oct_mean
    x_Nov = x[first_day_Nov:last_day_Nov] - nov_mean
    x_Dec = x[first_day_Dec:last_day_Dec] - dec_mean

    result = np.concatenate(np.array([x_Jan,x_Feb,x_Mar,x_Apr,x_May,x_Jun,x_Jul,x_Aug,x_Sep,x_Oct,x_Nov,x_Dec]))

    return result

# Function to
# (a) remove a trend from time series
# (b) normalize time series to zero mean and unit variance
def normalizer(ts):
    # Remove (linear) trend
    detrendedX = signal.detrend(ts)
    # Compute the mean
    mean = np.mean(detrendedX)
    # Compute the standard deviation
    std = np.std(detrendedX)
    # normalize to zero mean and unit variance
    zeroMean = detrendedX - mean
    result = zeroMean/std

    return result

# Lagged Pearson Correlation
# The time series x and y has to be normalized to zero mean and unit variance
# Tau is the lag considered
def laggedPearsonCorr(x, y, tau):
    # Length of time series
    n = len(x)
    # Consider then just (n - tau) values
    n_minus_tau = n - tau
    newX = x[0:n_minus_tau]
    # Drop the first tau elements from y
    newY = y[tau:]

    # Numerator
    numerator = np.sum(newX*newY)
    result = numerator/(n-1)

    return result

# Correlogram from -tau to tau
def laggedCorrelogram(x, y, tau):
    # Correlation between x and y from tau = 0 up to tau = tau

    # Initialize
    corr_x_to_y = []
    corr_y_to_x = []

    for i in arange(0,tau+1):
        x_to_y = laggedPearsonCorr(x,y,i)
        corr_x_to_y.append(x_to_y)

    for i in arange(1,tau+1):
        y_to_x = laggedPearsonCorr(y,x,i)
        corr_y_to_x.append(y_to_x)

    # Reverse the list y -> x
    corr_y_to_x.reverse()
    # Concatenate results
    lag_corr = corr_y_to_x + corr_x_to_y

    result = np.transpose([np.arange(-tau,tau+1,1),lag_corr])

    return result

# Define the Bartlett Formula

# As a first step you want the product of all autocorrelation values
# This is the numerator in the Bartlett formula
def bartlett_numerator(x,y):
    # Input x and y: two time series

    # Length of the time series
    length = len(x)
    # Autocorrelations of the first time series
    autocorr_x = laggedCorrelogram(x,x,length)
    # Autocorrelations of the second time series
    autocorr_y = laggedCorrelogram(y,y,length)
    # Summation term of the Bartlett formula
    summation = np.sum(autocorr_x[:,1]*autocorr_y[:,1])
    # Bartlett variance

    return summation

def bartlett_v(T, tau, numerator):
    # T is the length of the time series
    # tau is the lag
    # Summation is the sum of all autocorrelation products
    result = (1/float(T-tau))*numerator
    return result

# function significant
# inputs:
# time series x and y, lag tau_max, statistical sig. level alpha
# all_corr is a boolean whether to return all significant correlation (True)
# or only the max (False)
# outputs:
# The maximum (in abs value) statistical significant correlation
# (taking into account autocorrelations) and the correspondent lag

# The time series x and y should be normalized to zero mean and 1 std first

def significantCorr(x, y, tau_max, alpha, all_corr):
    # Length of time series
    T = len(x)
    # Compute the correlogram between x and y up to tau_max
    correlogram = laggedCorrelogram(x, y, tau_max)
    # Compute the numerator of the Bartlett variance
    bartlett_num = bartlett_numerator(x,y)
    # Compute the Bartlett variance from tau = -tau_max to tau = tau_max
    bartlettVariance = []

    for k in np.arange(-tau_max,tau_max+1):
        bartlettVariance.append(bartlett_v(T, k, bartlett_num))

    # Compute the Bartlett standard deviation
    bartlettSTD = np.sqrt(bartlettVariance)

    # Define the Z statistics
    zeta = np.abs(correlogram[:,1])/bartlettSTD

    # Length of z (it should be 2*tau + 1 if correct)
    len_z = len(zeta)

    # Find the p-values given a significance level alpha
    pValues = []
    for i in range(len_z):
        value = 1 - scipy.stats.norm(0, 1).cdf(zeta[i])
        pValues.append(value)
    pValues = np.array(pValues)

    # Position of the significant bastards
    # I add "[0]" in the end, if not the results is: (np.array(...))
    # While with the [0], is just np.array(...)

    position_Significant_Corr = np.where(pValues<alpha)[0]

    if len(position_Significant_Corr) == 0:
        result = array([[nan        , nan]])
    else:
        # Lets retrieve these statistical significant correlations

        # How many significant correlations
        sig_corr_number = len(position_Significant_Corr)
        #print(sig_corr_number)

        stat_sig_corr = np.zeros((sig_corr_number,2))

        for i in range(sig_corr_number):
            stat_sig_corr[i] = correlogram[position_Significant_Corr[i]]

        # Max in absolute value
        max_abs_sig_correlation = max(stat_sig_corr[:,1], key=abs)
        # Return the Max in absolute value and the correspondent lag
        result = stat_sig_corr[np.where(stat_sig_corr[:,1]==max_abs_sig_correlation)[0]]

        if all_corr == True:
           result = stat_sig_corr
    
    return result

