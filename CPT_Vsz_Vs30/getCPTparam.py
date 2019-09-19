# Author: Claire Dong
# Last modified: 30/08/2019

import numpy as np

def getCPTparam(z, qc, fs, u2):
    '''Compute basic CPT parameters'''    
    # compute pore pressure corretd tip resistance
    a = 0.8
    u2 = u2
    qt = qc - u2*(1-a)
    # assume soil unit weight (MN/m3)
    gamma = 0.00981 * 1.9
    # atmospheric pressure (MPa)
    pa = 0.1
    # groundwater table depth(m)
    gwt = 1.0
    # compute vertical stress profile 
    totalStress = np.zeros(len(z))
    u0 = np.zeros(len(z))
    for i in range(1, len(z)):
        totalStress[i] = gamma*(z[i]-z[i-1]) + totalStress[i-1]
        if z[i] >= gwt:
            u0[i] = 0.00981*(z[i]-z[i-1]) + u0[i-1]
    effStress = totalStress - u0
    effStress[0] = effStress[1] # fix error caused by dividing 0 
    
    # compute non-normalised Ic based on the correlation by Robertson (2010).  
    Rf = (fs/qc)*100
    Ic = ((3.47 - np.log10(qc/pa))**2 + (np.log10(Rf) + 1.22)**2)**0.5   
    n = 0.381*Ic + 0.05*(effStress/pa) - 0.15
    for i in range(0,len(n)):
        if n[i] > 1:
            n[i] = 1
    Qtn = ((qt-totalStress)/pa) * (pa/effStress)**n
    
    # note in Chris's code, Qtn is used instead of qc1n or qt1n
    # does not make that much of difference 
    qc1n = Qtn
    qt1n = Qtn
    return qt, Ic, Qtn, qc1n, qt1n, effStress