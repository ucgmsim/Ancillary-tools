# Author: Claire Dong
# Last modified: 30/08/2019

import numpy as np
from computeVs import computeVs

def computeVsz(filename, correlationName, correlationFlag):
    '''Calculate Vsz from randomly generated Vs profiles'''
    
    (z, randVs, Vs) = computeVs(filename, correlationName, correlationFlag)

    Vsz, Vsz_SD = compute_vsz_sigma_from_vs(Vs, randVs, z, correlationFlag)

    return z, Vsz, Vsz_SD


def compute_vsz_sigma_from_vs(Vs, randVs, z, correlationFlag):
    Vsz, max_depth = compute_vsz_from_vs(Vs, z)
    # the standard deviation is estimated based on randVs
    randVsz = []
    for k in range(0, len(randVs[0])):
        d = 0
        t = 0
        n = 0

        cur_depth = 0
        prev_depth = None
        cur_vs = prev_vs = Vs[0]

        while z[n] < max_depth:
            dn = z[n + 1] - z[n]
            vn = 0.5 * (randVs[n, k] + randVs[n + 1, k])  # velocity at mid point
            tn = dn / vn
            t += tn
            d += dn
            n += 1
        randVsz.append(d / t)
    # ------------------------Compute mean Vsz-----------------------------------
    if correlationFlag == 0:
        Vsz_SD = np.std(np.log(randVsz))

    elif correlationFlag == 1:
        Vsz_SD = np.std(np.log(randVsz))

    else:  # correlationFlag == 'partial'
        Vsz_SD = np.std(np.log(randVsz))

    return Vsz, Vsz_SD


def compute_vsz_from_vs(Vs, z):
    max_depth = int(z[-1])  # round down to the nearest integer
    # the mean Vsz is computed from Vs based on correlation
    d = 0
    t = 0
    n = 0
    cur_depth = 0
    prev_depth = None
    cur_vs = prev_vs = Vs[0]
    while cur_depth < max_depth:
        prev_depth = cur_depth
        cur_depth = z[n]
        dn = cur_depth - prev_depth

        prev_vs = cur_vs
        cur_vs = Vs[n]

        vn = 0.5 * (cur_vs + prev_vs)  # velocity at mid point
        tn = dn / vn
        t += tn
        d += dn
        n += 1
    Vsz = float(d / t)
    return Vsz, max_depth
