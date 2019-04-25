import numpy as np
from computeVsz import computeVsz

def computeVs30(z, qc, fs, u2, correlationName, correlationFlag):
    '''Calculate Vs30 from Vsz (Boore et al., 2011)
       This correlation does not consider the site class.
    '''
    
    (z, mu_Vsz, Vsz_SD) = computeVsz(z, qc, fs, u2, correlationName, correlationFlag)
    
    # Coeffecients: [C0; C1; C2; SD] where z = [5, 29]
    coeffs = np.array([[0.2046, 1.318, -0.1174, 0.119], [-0.06072, 1.482, -0.1423, 0.111],\
                      [-0.2744, 1.607, -0.1600, 0.103], [-0.3723, 1.649, -0.1634, 0.097],\
                      [-0.4941, 1.707, -0.1692, 0.090], [-0.5438, 1.715, -0.1667, 0.084],\
                      [-0.6006, 1.727, -0.1649, 0.078], [-0.6082, 1.707, -0.1576, 0.072],\
                      [-0.6322, 1.698, -0.1524, 0.067], [-0.6118, 1.659, -0.1421, 0.062],\
                      [-0.5780, 1.611, -0.1303, 0.056], [-0.5430, 1.565, -0.1193, 0.052],\
                      [-0.5282, 1.535, -0.1115, 0.047], [-0.4960, 1.494, -0.1020, 0.043],\
                      [-0.4552, 1.447, -0.09156, 0.038], [-0.4059, 1.396, -0.08064, 0.035],\
                      [-0.3827, 1.365, -0.07338, 0.030], [-0.3531, 1.331, -0.06585, 0.027],\
                      [-0.3158, 1.291, -0.05751, 0.023], [-0.2736, 1.250, -0.04896, 0.019],\
                      [-0.2227, 1.202, -0.03943, 0.016], [-0.1768, 1.159, -0.03087, 0.013],\
                      [-0.1349, 1.120, -0.02310, 0.009], [-0.09038, 1.080, -0.01527, 0.006],\
                      [-0.04612, 1.040, -0.007618, 0.003]])

    max_depth = int(z[-1]) 
    index = max_depth - 5
    (C0, C1, C2, SD) = coeffs[index]
    
    # Compute Vs30
    log = np.log10
    ln = np.log
    Vs30 = 10**(C0 + C1*log(mu_Vsz) + C2*(log(mu_Vsz))**2)
    # Compute Vs30 standard deviation
    Vsz = ln(mu_Vsz)    
    dVs30 = (C1*10**(C1*log(Vsz)) + 2*C2*log(Vsz)*10**(C2*log(Vsz)**2)) / Vsz
    Vs30_SD = np.sqrt(SD**2 + (dVs30**2)*(Vsz_SD)**2)
    
    return Vs30, Vs30_SD
        