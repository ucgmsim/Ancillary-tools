# Author: Claire Dong
# Last modified: 30/08/2019

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm, norm

def computePartialCor(z, Vs, Vs_SD, Nsim):
    
    # Pick a value for constant a
    rho_0 = 0.02
    h_0 = 5
    a = np.log(rho_0) / (-1*h_0)
    # Find the lag distance between each pair of values
    h = abs(np.subtract.outer(z, z))
    # Form the correlation rho (which is convaraince divded by standard deviation 
    # (in the range from 0 to 1)
    rho = np.exp(-1*a*h)
    # Form the covariance matrix (population standDev * rho * population standDev)
    sd = np.diag(Vs_SD.reshape(-1))
    Cov = np.dot(sd, np.dot(rho, sd))
    # Cholesky Decomposition to get lower triangular matrix
    L = np.linalg.cholesky(Cov)
    # Generate random uncorrelated numbers with Z~(0,1)
    rdUncorrVar = norm.rvs(loc=0, scale=1, size=((len(z)),Nsim))
    # Multiply by Chol(Cov) to generate random correlated numbers
    rdCorrVar = L @ rdUncorrVar
    # Adding the means to the random correlated variables
    randLnVs = (np.log(Vs) + rdCorrVar)
    # Return generated samples and log standard deviation
    randVs = np.exp(randLnVs)
    sigma = np.std(randLnVs)
    
    #-----------------Check--------------------
    # Check the sample means
    #print(np.mean(randLnVs,axis=1))
    #print(np.log(Vs))
    
    # Check the sample standard deviation
    #print(np.std(randLnVs, axis=1))
    #print(Vs_SD)
    
    # Check correlation matrix (might need to increase the number of sample)
    #print(np.corrcoef(randLnVs))
    #print(rho)
    
    
    return randVs, sigma

