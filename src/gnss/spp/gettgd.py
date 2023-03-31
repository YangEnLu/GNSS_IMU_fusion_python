from ...common.global_constants import glc, obsd, nav, default_opt
from ...common.satsys import satsys
import numpy as np


def gettgd(nav: nav, obs: obsd, opt: default_opt):
    dcb = np.zeros((glc().NFREQ, 1))
    sat = obs.sat
    sys, prn = satsys(sat)

    idx = nav.eph[:, 0] == sat
    if not np.any(idx):
        return dcb
    eph0 = nav.eph[idx, :]
    tgd1 = glc().CLIGHT*eph0[0, 34]
    tgd2 = glc().CLIGHT*eph0[0, 35]

    if sys == glc().SYS_GPS or sys == glc().SYS_QZS:
        gamma = (glc().FREQ_GPS_L1/glc().FREQ_GPS_L2)**2
        dcb[0, 0] = tgd1
        dcb[1, 0] = gamma*tgd1
    elif sys == glc().SYS_GAL:
        gamma = (glc().FREQ_GAL_E5A/glc().FREQ_GAL_E1)**2
        dcb[0, 0] = gamma*tgd1
        dcb[1, 0] = tgd1
        dcb[2, 0] = gamma*tgd1+(1-gamma)*tgd2
    elif sys == glc().SYS_BDS:
        if prn >= 18:  # BD3
            frq = opt.bd3frq
            for i in range(glc().NFREQ):
                if frq[i] == 1:
                    dcb[i, 0] = -tgd1
                elif frq[i] == 2:
                    dcb[i, 0] = 0
                elif frq[i] == 3:
                    dcb[i, 0] = 0
        else:  # BD2
            frq = opt.bd2frq
            for i in range(glc().NFREQ):
                if frq[i] == 1:
                    dcb[i, 0] = -tgd1
                elif frq[i] == 2:
                    dcb[i, 0] = -tgd2
                elif frq[i] == 3:
                    dcb[i, 0] = 0

    return dcb
