from .global_constants import glc
from .satsys import satsys
import numpy as np


def satexclude(sat, var, svh, opt):

    sys, prn = satsys(sat)
    if svh < 0:
        stat = 0
        return stat

    if sys == glc().SYS_QZS:
        svh = np.bitwise_and(svh, 254)
    if svh != 0:
        stat = 0
        return stat
    if var > 300**2:
        stat = 0
        return stat
    stat = 1
    return stat
