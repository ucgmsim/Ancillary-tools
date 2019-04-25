import numpy as np

def getCPTdata(filename):
    '''get CPT data and return [z; qc; fs; u2]'''
    data = np.loadtxt(filename, dtype=float, delimiter='	', skiprows=0, usecols=(0,1,2,3))
    data = data[(np.all(data[:,[0]]<30, axis=1)).T] # z is less then 30 m
    data = data[np.all(data[:,[1,2]]>0, axis=1)]    # delete rows with zero qc, fs
    z = data[:,0]                               # m
    qc = data[:,1]                              # MPa
    fs = data[:,2]                              # MPa
    u2 = data[:,3]                              # Mpa
    
    return z, qc, fs, u2