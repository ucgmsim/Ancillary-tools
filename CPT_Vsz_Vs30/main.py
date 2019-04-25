# Author: Claire Dong
# Last modified: 24/04/2019


import numpy as np
import matplotlib.pyplot as plt
from computeVs30 import computeVs30
from getCPTdata import getCPTdata

def main():
    '''get CPT data from NZGD'''
    #----------------------------Input-------------------------------
    # filenames
    filename = 'CCCC.txt'
    # correlation options: 'Andrus', 'Hegazy', 'McGann', 'Robertson'
    correlationNames = ['McGann', 'Andrus', 'Hegazy', 'Robertson']
    # Setup correlation flag for Vsz, choose 0 or 1
    correlationFlag = 0
    #-----------------------------------------------------------------
    
    (z, qc, fs, u2) = getCPTdata(filename)
    
    for correlationName in correlationNames:
        (Vs30, Vs30_SD) = computeVs30(z, qc, fs, u2, correlationName, correlationFlag)
        print("Expected Vs30 from '{0}' is: {1:.1f} m/s".format(correlationName, Vs30))
        print('Standard deviation for Vs30 is: {:.4f}\n'.format(Vs30_SD))
    
    
main()