import numpy as np
from ..common.global_constants import gtime


def timeadd(t0, sec):
    t0.sec = t0.sec+sec
    tt = np.floor(t0.sec)
    t = gtime()
    t.time = t0.time + np.fix(tt)
    t.sec = t0.sec-tt
    return t
