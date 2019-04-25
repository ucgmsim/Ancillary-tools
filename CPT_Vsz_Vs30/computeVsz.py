import numpy as np
from computeVs import computeVs

def computeVsz(z, qc, fs, u2, correlationName, correlationFlag):
    '''Calculate Vsz from randomly generated Vs profiles'''
    
    (z, randVs) = computeVs(z, qc, fs, u2, correlationName, correlationFlag)
    
    max_depth = int(z[-1]) # round down to the nearest integer
    Vsz = []
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
        Vsz.append(d/t)
    
    #------------------------Compute mean Vsz-----------------------------------
    if correlationFlag == 0:
        # Vsz is randomly distributed, E(X) = average
        mu_Vsz = np.mean(Vsz)
        Vsz_SD = np.std(np.log(Vsz))
    
    elif correlationFlag == 1:
        # Vsz has a log-normal distribution, E(X) = exp(mu+std^2/2)
        mu = np.mean(np.log(Vsz))
        Vsz_SD = np.std(np.log(Vsz))
        mu_Vsz = np.exp(mu+(Vsz_SD**2/2))
        
    print("Expected Vsz from '{0}' is: {1:.1f} m/s".format(correlationName, mu_Vsz))
    print('Standard deviation for Vsz is: {:.4f}'.format(Vsz_SD))  
    
    return z, mu_Vsz, Vsz_SD
