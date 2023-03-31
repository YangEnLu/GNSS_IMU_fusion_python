from .global_constants import glc
import numpy as np
from numpy.linalg import norm


def geodist(rs: np.ndarray, rr: np.ndarray):
    r = -1
    LOS = np.zeros((1, 3))

    if norm(rs) < glc().RE_WGS84:
        return r, LOS

    delta = rs - rr
    r = norm(delta)
    LOS = np.transpose(delta)/r
    r = r+glc().OMGE*(rs[0, 0]*rr[1, 0]-rs[1, 0]*rr[0, 0])/glc().CLIGHT
    
    return r, LOS
