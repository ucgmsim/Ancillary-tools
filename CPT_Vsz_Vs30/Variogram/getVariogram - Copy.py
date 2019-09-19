import numpy as np
from gstools import SRF, Exponential, Stable, vario_estimate_unstructured, CovModel, Gaussian
from gstools.covmodel.plot import plot_variogram
import matplotlib.pyplot as plt
import os
from getCPTdata import getCPTdata 
from computeVs import computeVs 


def getVariogram():
    # Extract each CPT filename
    termDepthFilename = os.path.abspath('Data\\Christchurch\\termDepthCPT.txt')
    cptFilePath = os.path.abspath("Data\\Christchurch\\processedCPTfiles")
    
    # Extract data
    IDlist = np.loadtxt(termDepthFilename, dtype=int, usecols=(0,3))    # CPT ID (1st col)
    IDlist = IDlist[(np.all(IDlist[:,[1]]>25, axis=1)).T]
    #IDlist = IDlist[(np.all(IDlist[:,[1]]<30, axis=1)).T]
    #print(IDlist)
    
    # correlation options: 'Andrus', 'Hegazy', 'McGann', 'Robertson', 'McGann2'
    correlationName = 'McGann'
    
    # Setup correlation flag for Vsz, choose from [0, 1, 'partial']
    correlationFlag = 'partial'
        
    
    #filelist = ["CCCC.txt", "CBGS.txt", "NBLC.txt"]#, "HVSC5.txt", "HVSC5.txt"]
    
    bin_width = 0.5
    bin_edges = np.arange(0, 30, bin_width)
    bin_no = len(bin_edges) - 1
    h = np.zeros(bin_no, dtype=float)
    variogram = np.zeros(bin_no, dtype=float)
    counts = np.zeros(bin_no, dtype=float)    
    
    for i in range(20):
    #for filename in filelist:
        ID = IDlist[i,0]
        filename = cptFilePath + "\\CPT_{0}.out".format(ID)
        (z, qc, fs, u2) = getCPTdata(filename)
        (z, randVs, Vs) = computeVs(z, qc, fs, u2, correlationName, correlationFlag)
    
              
    
        max_z = int(max(z))
        # estimate the variogram of the field with 40 bins
        bins = np.arange(0,max_z,bin_width)
        z = np.array([z])
        field = np.log(Vs).reshape(-1)
        bin_center, gamma = vario_estimate_unstructured(z, field, bins)
        plt.scatter(bin_center, gamma, s=1, label='data')
        
        '''
        gamma = np.array([gamma]).T
        gamma = gamma[np.all(gamma>0.001, axis=1)]
        gamma = gamma.reshape(-1)'''
        
        h[0:len(bin_center)] = h[0:len(bin_center)] + bin_center
        variogram[0:len(gamma)] = variogram[0:len(gamma)] + gamma
        counts[0:len(gamma)] = counts[0:len(gamma)] + 1
    
    
    print(counts)
    h = np.array([h]).T
    variogram = np.array([variogram]).T
    counts = np.array([counts]).T
    
    bin_mask = np.all(variogram>0.001, axis=1)


    h = h[bin_mask]

    variogram = variogram[bin_mask]
    
    counts = counts[bin_mask]
    
    h = h/counts
    variogram = variogram/counts
    h = h.reshape(-1)
    variogram = variogram.reshape(-1)
    
    
    
    # fit the variogram with a stable model. (no nugget fitted)
    fit_model = Exponential(dim=1)
    fit_model.fit_variogram(h, variogram, nugget=False)
    plt.plot(h, variogram, label='avg')
    plot_variogram(fit_model, x_max=max_z)
    # output
    print(fit_model)
    
    plt.show()
        
    
    '''
    rd_model = Exponential(dim=1, var=1)
    randVs = np.zeros((len(z), Nsim))
    for j in range(Nsim):
        srf = SRF(rd_model, mean=0)
        rd_field = srf(np.array([z])) * fit_model.var 

        for i in range(len(rd_field)):
            if rd_field[i] < 0:
                randVs[i,j] = (Vs[i]*np.exp(-1*np.sqrt(abs(rd_field[i]))))
            else:
                randVs[i,j] = (Vs[i]*np.exp(np.sqrt(rd_field[i])))
    '''
    


getVariogram()
