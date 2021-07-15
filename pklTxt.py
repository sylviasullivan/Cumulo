import pickle
import pandas as pd
import numpy as np

# Read in the pkl files and convert them to txt for use
# in Codes.
with open('Subdomains_1.pkl','rb') as f:
     subdomains = pickle.load(f)

for j in subdomains.columns:
    np.savetxt(j + '.txt',subdomains[j].values[0],fmt='%5.5f',delimiter=",")
