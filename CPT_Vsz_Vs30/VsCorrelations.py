import numpy as np
import matplotlib.pyplot as plt

def Vs_McGann(z, qc, fs):
    '''CPT-Vs correlaion developed by McGann et al. (2015b).
    qc, fs in kPa'''
    VsMcGann = np.array([18.4 * (qc*1000)**0.144 * (fs*1000)**0.083 * z**0.278]).T
    #standard deviation
    Vs_SD = np.zeros([len(z),1])
    for i in range(0, len(z)):
        if z[i] <= 5:
            Vs_SD[i] = 0.162
        elif z[i] > 5 and z[i] < 10:
            Vs_SD[i] = 0.216 - 0.0108*(z[i])
        else:
            Vs_SD[i] = 0.108
    return z, VsMcGann, Vs_SD


def Vs_Andrus(Ic, z, qt):
    '''CPT-Vs correlaion developed by Andrus et al. (2007).
    qt in kPa'''
    # Holocene-Age Soils, where ASF = 1
    VsAnd = np.array([2.27*((qt*1000)**0.412)*(Ic**0.989)*(z**0.033)]).T
    #residual standard deviation: suggests that 68% of the data fall within 24m/s.
    Vs_SD = np.log(24/VsAnd + 1)   
    return z, VsAnd, Vs_SD


def Vs_Robertson(z, Ic, Qtn, effStress):
    '''CPT-Vs correlaion developed by Robertson (2009).'''
    pa = 0.1
    alpha = 10**(0.55*Ic+1.68)
    VsRob = np.array([(alpha*Qtn)**0.5 * (effStress/pa)**0.25]).T
    #standard deviation(not available), set to 0.2
    Vs_SD = np.full((len(VsRob),1), 0.2)
    return z, VsRob, Vs_SD


def Vs_Hegazy(z, Ic, qc1n, effStress):
    '''CPT-Vs correlaion developed by Hegazy & Mayne(2006).'''
    pa = 0.1
    VsHegazy = np.array([0.0831*qc1n*(effStress/pa)**0.25*np.exp(1.786*Ic)]).T
    #standard deviation(not available), set to 0.2
    Vs_SD = np.full((len(VsHegazy),1), 0.2)
    return z, VsHegazy, Vs_SD     