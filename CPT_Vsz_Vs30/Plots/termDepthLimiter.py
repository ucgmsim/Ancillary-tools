import numpy as np
import os
from scipy.stats import norm

def writer_Vs30_termDepth():
    '''Converts a file which contains the estimates, and limits the estimates to only those which have more data
    a given height'''
    '''Write files that are used to plot_1to1_depth, which is classified by termination depth
    '''
    correlationName = 'McGann'
    bins = [5,10,15,20,25,30,999]
    summaryFile = os.path.abspath("..\\Results\\Christchurch\\{}_summary.txt".format(correlationName))
    
    # Extract terminationDepth, Vs30, Vs30_SD
    data = np.loadtxt(summaryFile, usecols=(3,4,5), skiprows=1)
    
    for i in range(len(bins)-1):
        Vs30 = data[(np.all(data[:,[0]]>=bins[i], axis=1))]
        Vs30 = Vs30[(np.all(Vs30[:,[0]]<bins[i+1], axis=1))]
        #print(Vs30)
        
        filename = os.path.abspath("Christchurch\\{0}_{1}to{2}m.txt".format(correlationName, bins[i], bins[i+1]))
        f = open(filename, "w+")
        f.write("{0}\t{1}\t{2}\t{3}\n".format('Vs30', 'standDev', 'lowerBound', 'upperBound'))
        if len(Vs30) > 0:
            lowerBound = np.exp(np.log(Vs30[:,1]) - Vs30[:,2])
            upperBound = np.exp(np.log(Vs30[:,1]) + Vs30[:,2])
            for j in range(len(lowerBound)):
                f.write("{0} {1} {2} {3}\n".format(Vs30[j,1], Vs30[j,2], lowerBound[j], upperBound[j]))
            
writer_Vs30_termDepth()