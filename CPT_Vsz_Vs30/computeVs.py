# Author: Claire Dong
# Last modified: 30/08/2019

from scipy.stats import lognorm, norm
import numpy as np
import matplotlib.pyplot as plt
from getCPTparam import getCPTparam
from getVsCorrelations import Vs_McGann, Vs_Robertson, Vs_Andrus, Vs_Hegazy, Vs_McGann2
from computePartialCor import computePartialCor
from getCPTdata import getCPTdata
import os


def computeVs(filename, correlationName, correlationFlag):
    '''compute Vs from CPT data'''
    
    (z, qc, fs, u2) = getCPTdata(filename)
    
    (qt, Ic, Qtn, qc1n, qt1n, effStress) = getCPTparam(z, qc, fs, u2)
    
    if correlationName == 'McGann':
        (z, Vs, Vs_SD) = Vs_McGann(z, qc, fs)
        
    elif correlationName == 'Andrus':
        (z, Vs, Vs_SD) = Vs_Andrus(Ic, z, qt)
        
    elif correlationName == 'Robertson':
        (z, Vs, Vs_SD) = Vs_Robertson(z, Ic, Qtn, effStress)
        
    elif correlationName == 'Hegazy':
        (z, Vs, Vs_SD) = Vs_Hegazy(z, Ic, qc1n, effStress)
        
    elif correlationName == 'McGann2':
        (z, Vs, Vs_SD) = Vs_McGann2(z, qc, fs)
        
    else:
        print('Please input valid correlation names.')
        
    # assume the Vs in the first 1m is constant
    i = 0
    while z[i] < 1.5:
        i += 1
    Vs[0:i] = Vs[i]

    #-----------------Compute random selected Vs---------------------
    Nsim = 50
    if correlationFlag == 0:
        lnVs = np.log(Vs)
        randLnVs = norm.rvs(loc=lnVs, scale=Vs_SD, size=(len(Vs),Nsim))
        sigma = np.std(randLnVs)
        randVs = np.exp(randLnVs)

        
    elif correlationFlag == 1:
        # Generate the first Vs and applt its variance to the rest
        lnVs = np.log(Vs)
        randLnVs = norm.rvs(loc=lnVs[0], scale=Vs_SD[0], size=Nsim)
        z_score = (randLnVs - lnVs[0]) / Vs_SD[0]
        randLnVs = Vs_SD * z_score + lnVs
        randVs = np.exp(randLnVs)
        sigma = np.std(randLnVs)

        
    elif correlationFlag == 'partial':
        randVs, sigma = computePartialCor(z, Vs, Vs_SD, Nsim)
        
        
    else:
        print('Please input valid correlation flag.')
    
    #---------------------------Plotting--------------------------------
    '''
    # Compute the upper and lower bound standard deviations
    lowerVs = np.exp(np.log(Vs) - sigma)
    upperVs = np.exp(np.log(Vs) + sigma)
    
        
    # Plot all the random selected samples
    Vs_file = os.path.abspath("CBGSmasw.dat")
    measure_z = np.loadtxt(Vs_file, dtype=float, skiprows=0, usecols=(0))
    measure_Vs = np.loadtxt(Vs_file, dtype=float, skiprows=0, usecols=(-1))
    plt.figure()
    plt.grid(linestyle=':')
    plt.plot(measure_Vs, measure_z, label='SW-Vs', color='b')      
    plt.plot(Vs, z, label='CPT-Vs', color='r')
    plt.plot(lowerVs, z, color='r', alpha=0.3)
    plt.plot(upperVs, z, color='r', alpha=0.3)
    plt.xlabel('Vs {}'.format(correlationName))
    plt.ylabel('z (m)')
    plt.xlim(0, 600)
    plt.ylim(0, 30)
    plt.legend()
    plt.text(700, 1.5, '(g)', weight='bold')
    plt.xticks([0, 200, 400, 600])
    plt.gca().invert_yaxis()
    plt.gca().set_aspect(50)
    plt.show()
    '''
    #------------------------------------------------------------------
    
    return z, randVs, Vs