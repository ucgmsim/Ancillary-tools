from scipy.stats import lognorm
import numpy as np
import matplotlib.pyplot as plt
from getCPTparam import getCPTparam
from VsCorrelations import Vs_McGann, Vs_Robertson, Vs_Andrus, Vs_Hegazy

def computeVs(z, qc, fs, u2, correlationName, correlationFlag):
    '''compute Vs from CPT data'''
    (qt, Ic, Qtn, qc1n, qt1n, effStress) = getCPTparam(z, qc, fs, u2)
    
    if correlationName == 'McGann':
        (z, Vs, Vs_SD) = Vs_McGann(z, qc, fs)
        
    elif correlationName == 'Andrus':
        (z, Vs, Vs_SD) = Vs_Andrus(Ic, z, qt)
        
    elif correlationName == 'Robertson':
        (z, Vs, Vs_SD) = Vs_Robertson(z, Ic, Qtn, effStress)
        
    elif correlationName == 'Hegazy':
        (z, Vs, Vs_SD) = Vs_Hegazy(z, Ic, qc1n, effStress)
        
    else:
        print('Please input valid correlation names.')
        
    # assume the Vs in the first 1m is constant
    i = 0
    while z[i] < 1 or Vs[i] > 300:
        i += 1
    Vs[0:i] = Vs[i]

    #-----------------Compute random selected Vs---------------------
    Nsim = 50
    if correlationFlag == 0:
        randVs = lognorm.rvs(s=Vs_SD, scale=Vs, size=(len(Vs),Nsim))      
        
    elif correlationFlag == 1:
        # Generate the first Vs from a log-normal distribution 
        randVs = lognorm.rvs(s=Vs_SD[0], scale=Vs[0], size=Nsim)
        # Calculate the residual StandDev and log-normal StandDev for each realization
        residual_std = randVs - Vs[0]
        lnStd = np.log(residual_std/Vs[0] + 1)
        randVs = Vs*np.exp(lnStd)

    else:
        print('Please input valid correlation flag.')
        
    #---------------------------Plotting--------------------------------
    #This part is only for plotting, does not involved in any calculations
    mu_Vs = np.zeros(len(randVs[:,0]))
    if correlationFlag == 0:
        for i in range(len(randVs[:,0])):
            # Vs is randomly distributed, E(X) = average
            mu_Vs[i] = np.mean(randVs[i,:])
    
    elif correlationFlag == 1:
        for i in range(len(randVs[:,0])):
            # Vs has a log-normal distribution, E(X) = exp(mu+std^2/2)     
            mu = np.mean(np.log(randVs[i,:]))
            sigma = np.std(np.log(randVs[i,:]))
            mu_Vs[i] = np.exp(mu+(sigma**2/2))
    
    # Plot all the random selected samples
    Vs_file = 'CCCCmasw.dat'
    measure_z = np.loadtxt(Vs_file, dtype=float, delimiter=' ', skiprows=0, usecols=(0))
    measure_Vs = np.loadtxt(Vs_file, dtype=float, delimiter=' ', skiprows=0, usecols=(-1))
    plt.figure()
    plt.plot(mu_Vs, z, label='expected Vs')
    plt.plot(measure_Vs, measure_z, label='measured Vs')
    plt.plot(Vs, z, label='Vs from correlation')
    plt.title("Vs profiles from '{1}' ({0})".format(Vs_file, correlationName))
    plt.xlabel('Vs (m/s)')
    plt.ylabel('z (m)')
    plt.xlim(0)
    plt.ylim(0)
    plt.legend()
    plt.gca().invert_yaxis()  
    #------------------------------------------------------------------
    
    return z, randVs