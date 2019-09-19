# Author: Claire Dong
# Editor: David van Drimmelen
# Last modified: 30/08/2019

from computeVs30 import computeVs30
import numpy as np
import os


def CPT_Vs30_main():
    '''Produce a text file of the new Vs30 estimates which can be used to plot on a map'''
    
    #----------------------------Input-------------------------------  
    # correlation options: 'Andrus', 'Hegazy', 'McGann', 'Robertson', 'McGann2'
    correlationName = 'McGann'
    
    # Setup correlation flag for Vsz, choose from [0, 1, 'partial']
    correlationFlag = 'partial'
    
    # Extract CPT filenames
    termDepthFilename = os.path.abspath('Data\\Christchurch\\termDepthCPT.txt')
    cptFilePath = os.path.abspath("Data\\Christchurch\\processedCPTfiles")
    IDlist = np.loadtxt(termDepthFilename, dtype=int, usecols=0)         # CPT ID (1st col)
    longList = np.loadtxt(termDepthFilename, dtype=float, usecols=1)     # longitude (2nd col)
    latList = np.loadtxt(termDepthFilename, dtype=float, usecols=2)      # latitude (3rd col)
    termDepthList = np.loadtxt(termDepthFilename, dtype=float, usecols=3)    # termination depth (4th col)
    
    # Open a file for writing--------------------------------------------------------------------
    
    summaryFile = os.path.abspath("Results\\Christchurch\\{}_summary.txt".format(correlationName))
    f = open(summaryFile, "a")
    f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format('ID', 'longitude', 'latitude', 'termDepth', 'Vs30', 'standDev'))
    
    start_index = 0
    end_index = len(IDlist)
    for i in range(start_index, end_index):
        ID = IDlist[i]
        long = longList[i]
        lat = latList[i]
        termDepth = termDepthList[i]
        filename = cptFilePath + "\\CPT_{0}.out".format(ID)
        (z, Vs30, Vs30_SD) = computeVs30(filename, correlationName, correlationFlag)
        #f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(ID, long, lat, termDepth, Vs30, Vs30_SD))
        print('CPT{} has been processed'.format(ID))
        print(z[-1], Vs30, Vs30_SD)


    #----------------------------------------------------------------------------------------------
    print('Completed...')


CPT_Vs30_main()