import numpy as np


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


coeffs = np.array(
    [
        [0.2046, 1.318, -0.1174, 0.119],
        [-0.06072, 1.482, -0.1423, 0.111],
        [-0.2744, 1.607, -0.1600, 0.103],
        [-0.3723, 1.649, -0.1634, 0.097],
        [-0.4941, 1.707, -0.1692, 0.090],
        [-0.5438, 1.715, -0.1667, 0.084],
        [-0.6006, 1.727, -0.1649, 0.078],
        [-0.6082, 1.707, -0.1576, 0.072],
        [-0.6322, 1.698, -0.1524, 0.067],
        [-0.6118, 1.659, -0.1421, 0.062],
        [-0.5780, 1.611, -0.1303, 0.056],
        [-0.5430, 1.565, -0.1193, 0.052],
        [-0.5282, 1.535, -0.1115, 0.047],
        [-0.4960, 1.494, -0.1020, 0.043],
        [-0.4552, 1.447, -0.09156, 0.038],
        [-0.4059, 1.396, -0.08064, 0.035],
        [-0.3827, 1.365, -0.07338, 0.030],
        [-0.3531, 1.331, -0.06585, 0.027],
        [-0.3158, 1.291, -0.05751, 0.023],
        [-0.2736, 1.250, -0.04896, 0.019],
        [-0.2227, 1.202, -0.03943, 0.016],
        [-0.1768, 1.159, -0.03087, 0.013],
        [-0.1349, 1.120, -0.02310, 0.009],
        [-0.09038, 1.080, -0.01527, 0.006],
        [-0.04612, 1.040, -0.007618, 0.003],
    ]
)


def get_coeffs(z):
    max_depth = int(z[-1])
    index = max_depth - 5
    if index < 0:
        raise IndexError("CPT is not deep enough")
    (C0, C1, C2, SD) = coeffs[index]
    return C0, C1, C2, SD


def vsz_to_vs30(Vsz, z):
    C0, C1, C2, SD = get_coeffs(z)
    # Compute Vs30
    Vs30 = 10 ** (C0 + C1 * np.log10(Vsz) + C2 * (np.log10(Vsz)) ** 2)
    return Vs30


def vsz_to_vs30_sigma(Vsz, Vsz_SD, z):
    # Compute Vs30 standard deviation
    C0, C1, C2, SD = get_coeffs(z)
    Vsz = np.log(Vsz)
    dVs30 = (
                    C1 * 10 ** (C1 * np.log10(Vsz))
                    + 2 * C2 * np.log10(Vsz) * 10 ** (C2 * np.log10(Vsz) ** 2)
            ) / Vsz
    Vs30_SD = np.sqrt(SD ** 2 + (dVs30 ** 2) * (Vsz_SD) ** 2)
    return Vs30_SD