# Cumulo

The initial goal of this project was to identify the spatiotemporal scales over which shallow and deep cloud coverage are significantly correlated/anti-correlated in the tropics and to explain why in terms of environmental variables. We use [Cumulo](https://arxiv.org/pdf/1911.04227.pdf) cloud classifications and ERA5 environmental variables - surface evaporation, surface/2-m temperature, and pressure velocity (w) - and looks at their time-lagged autocorrelations. We also run [delta-maps](https://arxiv.org/pdf/1602.07249.pdf) and [community detection](https://www.nature.com/articles/srep30750) algorithms (The second link is not the exact algorithm that Fabri used; I need to ask him to link it.) on these classifications and environmental variables for dimensionality reduction, i.e. to identify spatial domains over which the fields temporally evolve in a similar manner. Finally, we establish causal links between time series of the cloud classifications and environmental conditions in these delta-map domains or communities using the [Tigramite](https://github.com/jakobrunge/tigramite) causality algorithm. 

In the full version of this project, available upon request, data are stored in the following directories: *classifications* hold the Cumulo classifications month-by-month or the full year and at native resolution and remapped to 0.5-deg; *partitions* hold the time series of cloud cover over the 'partitions' shown at the bottom of the README; *delta-map-domains* hold the output of the delta-maps algorithm (e.g. the domain ID of each grid cell is given in the delta_domain_map* files and delta_domain_border* consists of 1's for domain boundaries and 0's elsewhere); and *communities* hold the output of the community detection algorithm.

Going forward, we are also interested to look at correlation/anti-correlation of the cloud classifications and environmental conditions in relation to anomalies in the tropical radiation budget as in [Bony et al. 2020](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019AV000155) but at daily rather than monthly timescales.

*plot_delta_maps.ipynb* - Notebook for visualization of the delta-map domains (Author: FF)

*preprocessing.ipynb* - Notebook for visualization of the standard deviation of the environmental variable and cloud fields and remove of grid cells with more than 70% nan values

### Scripts for correlograms and causality analysis with time series of cloud classifications and environmental variables

*correlogram_partitions.py*, *correlogram_partitions_significant.py*, *correlogram_parititons_nomax.py* - Plot the correlograms (time-lagged correlations of +/- 30 days) of deep convective (DC), stratocumulus (Sc), and cumulus (CU) cloud occurrence. *_significant.py* highlights only the statistically significant correlations, and the latter uses the *nomax* version of the numerical tools below. Ultimately the latter two can be combined with the first for a single correlogram file.

*splitDomains.py* - Extract a time series of cloud classification for a partition / domain

*Tigramite_Process_\*.ipynb* - A Python notebook with introductory use of the Tigramite causality algorithm library (Author: FF)

*communities_Tigramites.ipynb* - Adapated from the above, a Python notebook to identify causal relationships between DC, Sc, and CU cover as well as environmental variables (surface evaporation, surface temperature, and pressure velocity) in various communities (Author: SS)

### Scripts to download ERA5 data

*ERA5_\<var\>Retrieve* - Python script with Climate Data Store (cds) download specifications for variable \<var\>

*submit_\<var\>request.sh* - sbatch submission of the *ERA5_\<var\>Retrieve* script to download variable \<var\>

### Numerical and formatting utilities

*numerical_tools.py*, *numerical_tools_multid.py*, *numerical_tools_nomax.py* - A series of utility functions to plot correlograms and calculate the statistical significances of these time-lagged correlations (Bartlett function). The second handles data with multiple dimensions and the third omits correlations that are not significant; ultimately, the latter two can be combined with the first for a single utility file.

*convertNPYNC.py* - Utility to convert values from numpy output files to a NetCDF format

*community_stack.py* - Utility to reformat the output of the community detection algorithm

*pklTxt.py* - itty bitty utility to transform pickles into txt files

[partitions](partitions_map.png)
