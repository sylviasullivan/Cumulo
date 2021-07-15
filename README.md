# Cumulo

## Scripts for correlograms and causality analysis with time series of cloud classifications and environmental variables

*correlogram_partitions.py*, *correlogram_partitions_significant.py*, *correlogram_parititons_nomax.py* - Plot the correlograms (time-lagged correlations of +/- 30 days) of deep convective (DC), stratocumulus (Sc), and cumulus (CU) cloud occurrence. *_significant.py* highlights only the statistically significant correlations, and the latter uses the *nomax* version of the numerical tools below. Ultimately the latter two can be combined with the first for a single correlogram file.

*splitDomains.py* - Extract a time series of cloud classification for a partition / domain

*Tigramite_Process_\*.ipynb* - A Python notebook with introductory use of the Tigramite causality algorithm library (Author: FF)

*communities_Tigramites.ipynb* - Adapated from the above, a Python notebook to identify causal relationships between DC, Sc, and CU cover as well as environmental variables (surface evaporation, surface temperature, and pressure velocity) in various communities (Author: SS)

## Scripts to download ERA5 data

*ERA5_\<var\>Retrieve* - Python script with Climate Data Store (cds) download specifications for variable \<var\>

*submit_\<var\>request.sh* - sbatch submission of the *ERA5_\<var\>Retrieve* script to download variable \<var\>

## Numerical and formatting utilities

*numerical_tools.py*, *numerical_tools_multid.py*, *numerical_tools_nomax.py* - A series of utility functions to plot correlograms and calculate the statistical significances of these time-lagged correlations (Bartlett function). The second handles data with multiple dimensions and the third omits correlations that are not significant; ultimately, the latter two can be combined with the first for a single utility file.

*convertNPYNC.py* - Utility to convert values from numpy output files to a NetCDF format

*community_stack.py* - Utility to reformat the output of the community detection algorithm

*pklTxt.py* - itty bitty utility to transform pickles into txt files
