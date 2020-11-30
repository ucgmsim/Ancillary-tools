# Author: Claire Dong
# Last modified: 30/08/2019

from computeVsz import computeVsz

from Ancillary_tools.CPT_Vsz_Vs30.calculations import vsz_to_vs30, vsz_to_vs30_sigma


def computeVs30(filename, correlationName, correlationFlag):
    """Calculate Vs30 from Vsz (Boore et al., 2011)
       This correlation does not consider the site class.
    """

    (z, Vsz, Vsz_SD) = computeVsz(filename, correlationName, correlationFlag)

    # Coeffecients: [C0; C1; C2; SD] where z = [5, 29]
    Vs30 = vsz_to_vs30(Vsz, z)
    Vs30_SD = vsz_to_vs30_sigma(Vsz, Vsz_SD, z)

    return z, Vs30, Vs30_SD


