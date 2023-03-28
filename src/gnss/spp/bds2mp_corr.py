from ...common.global_constants import glc
from ...common.satsys import satsys
import numpy as np


def bds2mp_corr(rtk, obsr):
    IGSOCOEF = np.array([[-0.55, -0.40, -0.34, -0.23, -0.15, -0.04, 0.09, 0.19, 0.27, 0.35],
                         [-0.71, -0.36, -0.33, -0.19, -0.14, -
                             0.03, 0.08, 0.17, 0.24, 0.33],
                         [-0.27, -0.23, -0.21, -0.15, -0.11, -0.04, 0.05, 0.14, 0.19, 0.32]])

    MEOCOEF = np.array([[-0.47, -0.38, -0.32, -0.23, -0.11, 0.06, 0.34, 0.69, 0.97, 1.05],
                        [-0.40, -0.31, -0.26, -0.18, -0.06,
                            0.09, 0.28, 0.48, 0.64, 0.69],
                        [-0.22, -0.15, -0.13, -0.10, -0.04, 0.05, 0.14, 0.27, 0.36, 0.47]])

    nobs = np.shape(obsr)[0]

    for i in range(nobs):
        sat = obsr[i, 0].sat
        sys, prn = satsys(sat)
        if sys != glc().SYS_BDS:
            continue
        if prn <= 5:
            continue

        el = rtk.sat[sat-1, 0].azel[0, 1]*glc().R2D
        if el <= 0:
            continue

        dmp = np.zeros((1, 3))

        a = el*0.1
        b = np.fix(a)

        if int(prn) in glc().BD2_IGSO:
            if b < 0:
                for j in range(3):
                    dmp[0, j] = IGSOCOEF[j, 0]
            elif b >= 9:
                for j in range(3):
                    dmp[0, j] = IGSOCOEF[j, 9]
            else:
                for j in range(3):
                    dmp[0, j] = IGSOCOEF[j, b]*(1-a+b)+IGSOCOEF[j, b+1]*(a-b)
        elif int(prn) in glc().BD2_MEO:
            if b < 0:
                for j in range(3):
                    dmp[0, j] = MEOCOEF[j, 0]
            elif b >= 9:
                for j in range(3):
                    dmp[0, j] = MEOCOEF[j, 9]
            else:
                for j in range(3):
                    dmp[0, j] = MEOCOEF[j, b]*(1-a+b)+MEOCOEF[j, b+1]*(a-b)

        for j in range(3):
            obsr[i, 0].P[j, 0] = obsr[i, 0].P[j, 0]+dmp[0, j]

    return obsr
