# Author: Claire Dong
# Last modified: 30/08/2019

import numpy as np
from computeVs import computeVs

def computeVsz(filename, correlationName, correlationFlag):
    '''Calculate Vsz from randomly generated Vs profiles'''
    
    (z, randVs, Vs) = computeVs(filename, correlationName, correlationFlag)
    
    max_depth = int(z[-1]) # round down to the nearest integer
    
    # the mean Vsz is computed from Vs based on correlation
    d = 0
    t = 0
    n = 0
    while z[n] < max_depth:
        dn = z[n+1] - z[n]
        vn = 0.5*(Vs[n] + Vs[n+1])      # velocity at mid point 
        tn = dn / vn
        t += tn
        d += dn
        n += 1
    Vsz = float(d/t)
    
    # the standard deviation is estimated based on randVs
    randVsz = []    
    for k in range(0, len(randVs[0])):
        d = 0
        t = 0
        n = 0
        while z[n] < max_depth:
            dn = z[n+1] - z[n]
            vn = 0.5*(randVs[n,k] + randVs[n+1,k])      # velocity at mid point 
            tn = dn / vn
            t += tn
            d += dn
            n += 1
        randVsz.append(d/t)
    

    #------------------------Compute mean Vsz-----------------------------------
    if correlationFlag == 0:
        Vsz_SD = np.std(np.log(randVsz))
    
    elif correlationFlag == 1:
        Vsz_SD = np.std(np.log(randVsz))
        
    elif correlationFlag == 'partial':
        Vsz_SD = np.std(np.log(randVsz))

    return z, Vsz, Vsz_SD
