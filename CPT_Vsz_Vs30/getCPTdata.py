# Author: Claire Dong
# Last modified: 30/08/2019

import numpy as np

def getCPTdata(filename):
    '''get CPT data and return [z; qc; fs; u2]'''
    data = np.loadtxt(filename, dtype=float, delimiter=",", skiprows=1)
    data = data[(np.all(data[:,[0]]<30, axis=1)).T] # z is less then 30 m
    data = data[np.all(data[:,[1,2]]>0, axis=1)]    # delete rows with zero qc, fs
    z_raw = data[:,0]                               # m
    qc_raw = data[:,1]                              # MPa
    fs_raw = data[:,2]                              # MPa
    u2_raw = data[:,3]                              # Mpa
    
    downsize = np.arange(z_raw[0],30,0.02)
    z = np.array([])
    qc = np.array([])
    fs = np.array([])
    u2 = np.array([])
    for j in range(len(downsize)):
        for i in range(len(z_raw)):
            if abs(z_raw[i] - downsize[j]) < 0.001:
                z = np.append(z, z_raw[i])
                qc = np.append(qc, qc_raw[i])
                fs = np.append(fs, fs_raw[i])
                u2 = np.append(u2, u2_raw[i])
                
    if len(u2) > 50:
        while u2[50] >= 10:
            u2 = u2/1000    #account for differing units

    # some units are off - so need to see if conversion is needed
    if len(fs) > 100:
        # Account for differing units
        if fs[100] > 1.0:
            fs = fs/1000
    elif len(fs) > 5:
        if fs[5] > 1.0:
            fs = fs/1000        
    else:
        fs = fs
        
            
    
    return z, qc, fs, u2
