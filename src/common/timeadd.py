import numpy as np
from ..common.global_constants import gtime


def timeadd(t0:gtime, sec:float):
    t0_ = gtime()
    t0_.time = t0.time
    t0_.sec = t0.sec+sec
    
    tt = np.floor(t0_.sec)
    
    t = gtime()
    t.time = t0_.time + np.fix(tt)
    t.sec = t0_.sec-tt
    return t
