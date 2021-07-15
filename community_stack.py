import numpy as np
import os,sys

basedir = '/scratch/b/b380873/Cumulo/communities/'

# Cirrus communities
cdir = basedir + 'cirrus/signals/'

# Store a list of all files in the cirrus signals directory.
_, _, fi_list = next(os.walk(cdir))

# Use the first signal file to initialize the matrix that will hold everything.
M_all = np.genfromtxt(cdir + fi_list[0])

# Iterate through the remaining signal files and stack them into the matrix.
for fi in fi_list[1:]:
    A = np.genfromtxt(cdir + fi)
    M_all = np.vstack((M_all,A))

# Stack in the low-cloud community signals.
variables = ['low_clouds','se','T2m']
for v in variables:
    cdir = basedir + v + '/signals/'
    _, _, fi_list = next(os.walk(cdir))
    for fi in fi_list:
        A = np.genfromtxt(cdir + fi)
        M_all = np.vstack((M_all,A))

# Sanity check at the end. We have 12 cirrus and low-cloud communities, 9 T2m ones,
# and 4 surface evap ones. We take the transpose and M_all has shape (366 days, 37 signals)
print('Matrix final shape: ' + str(M_all.T.shape))
np.save('community_signals_all.npy',M_all.T)
