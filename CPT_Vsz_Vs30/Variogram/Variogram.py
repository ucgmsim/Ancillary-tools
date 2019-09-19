import numpy as np
import os
from getCPTdata import getCPTdata 
from computeVs import computeVs 
#from gstools import SRF, Exponential, Stable, vario_estimate_unstructured, CovModel, Gaussian
#from gstools.covmodel.plot import plot_variogram
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, b, c):
    return a * np.exp(-b * x) + c    


def Variogram():   
    # Extract each CPT filename
    termDepthFilename = os.path.abspath('Data\\Christchurch\\termDepthCPT.txt')
    cptFilePath = os.path.abspath("Data\\Christchurch\\processedCPTfiles")
    
    # Extract data
    IDlist = np.loadtxt(termDepthFilename, dtype=int, usecols=0)            # CPT ID (1st col)
    
    # correlation options: 'Andrus', 'Hegazy', 'McGann', 'Robertson', 'McGann2'
    correlationName = 'McGann'
    
    # Setup correlation flag for Vsz, choose from [0, 1, 'partial']
    correlationFlag = 'partial'
        
    
    #start_index =100
    #end_index = len(IDlist)
    #end_index = 101
    filelist = ["CBGS.txt", "CCCC.txt", "NBLC.txt"]#, "HVSC5.txt", "HVSC5.txt"]
    
    #for i in range(start_index, end_index):
    for filename in filelist:
        #ID = IDlist[i]
        #filename = cptFilePath + "\\CPT_{0}.out".format(ID)
        #filename = 'HVSC1.txt'
        (z, qc, fs, u2) = getCPTdata(filename)
        (z, randVs, Vs) = computeVs(z, qc, fs, u2, correlationName, correlationFlag)
        
        
        z = np.array([z]).T
        Vs = Vs[(np.all(z>=1.5, axis=1))]
        z = z[(np.all(z>=1.5, axis=1))]
        Vs = np.log(Vs)
        bin_edges = np.arange(0, 6, 0.1)
        bin_no = len(bin_edges) - 1
        h = np.zeros(bin_no, dtype=float)
        variogram = np.zeros(bin_no, dtype=float)
        counts = np.zeros(bin_no, dtype=float)
        
        
        # Referece: '...\Python\Python37-32\Lib\site-packages\gstools\variogram\py_estimator' 
        # calculate all field value differences and square it
        #Vs = Vs.reshape(-1)
        #z = np.array([z]).reshape(-1)
        #field_diff_quad = np.subtract.outer(Vs, Vs) ** 2    
        # calculate all distances
        #distance = abs(np.subtract.outer(z, z))

        
        for j in range(len(z)):
            for k in range(j, len(z)):
                distance = abs(z[j] - z[k])
                diff_squad = 0.5*(Vs[j] - Vs[k])**2                
                
                # iterate over all bins
                for q in range(bin_no):
                    if distance >= bin_edges[q] and distance < bin_edges[q+1]:
                        counts[q] += 1
                        variogram[q] += diff_squad
                        h[q] += distance
        
        print('done')
        
    for p in range(len(h)):
        if counts[p] != 0:
            variogram[p] = variogram[p]/counts[p]
            h[p] = h[p]/counts[p]
    
    
    plt.figure()
    plt.scatter(h, variogram, s=1, label='data')
    plt.legend()
    plt.show()
    
    plt.figure()
    popt, pcov = curve_fit(func, h, variogram)
    print(popt)
    print(pcov)
    x = np.linspace(0, 6, 200)
    y = func(x, popt[0], popt[1], popt[2])
    print(func(5, popt[0], popt[1], popt[2])/y[-1])
    plt.plot(x, y, color='r', label='gamma(h) = {0:.3f} * exp(-{1:.3f} * x) + {2:.3f}'.format(popt[0], popt[1], popt[2]))
    plt.scatter(h, variogram, s=1, label='data')
    plt.legend()
    plt.show()


    
    
    '''
    max_z = int(max(z))
    # estimate the variogram of the field with 40 bins
    bins = np.arange(0,max_z,1)
    z = np.array([z])
    print(z)
    field = Vs.reshape(-1)
    bin_center, gamma = vario_estimate_unstructured(z, field, bins)
    plt.plot(bin_center, gamma)
    
    # fit the variogram with a stable model. (no nugget fitted)
    fit_model = Exponential(dim=1)
    fit_model.fit_variogram(bin_center, gamma, nugget=False)
    plot_variogram(fit_model, x_max=max_z)
    # output
    print(fit_model)
    plt.show()
    '''
    
    
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


Variogram()
