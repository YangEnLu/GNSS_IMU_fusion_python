from ...common.global_constants import glc, gtime, default_opt
import numpy as np
from numpy.linalg import inv
from ...common.time2gpst import time2gpst


def valsol(time: gtime, v, P, vsat, Q, opt: default_opt):
    chisqr = np.array([[10.8, 13.8, 16.3, 18.5, 18.5, 22.5, 24.3, 26.1, 27.9, 29.6,
                       31.3, 32.9, 34.5, 36.1, 37.7, 39.3, 40.8, 42.3, 43.8, 45.3,
                       46.8, 48.3, 49.7, 51.2, 52.6, 54.1, 55.5, 56.9, 58.3, 59.7,
                       61.1, 62.5, 63.9, 65.2, 66.6, 68.0, 69.3, 70.7, 72.1, 73.4,
                       74.7, 76.0, 77.3, 78.6, 80.0, 81.3, 82.6, 84.0, 85.4, 86.7,
                       88.0, 89.3, 90.6, 91.9, 93.3, 94.7, 96.0, 97.4, 98.7, 100,
                       101, 102, 103, 104, 105, 107, 108, 109, 110, 112,
                       113, 114, 115, 116, 118, 119, 120, 122, 123, 125,
                       126, 127, 128, 129, 131, 132, 133, 134, 135, 137,
                       138, 139, 140, 142, 143, 144, 145, 147, 148, 149]])

    stat = 1
    nx = 3+glc().NSYS

    # chi-square test for residuals
    nv = np.shape(v)[0]
    var = inv(P)
    for i in range(nv):
        v[i, 0] = v[i, 0]/np.sqrt(var[i, i])
    v_ = np.reshape(v, -1)
    if nv > nx and np.dot(v_, v_) > chisqr[0, int(nv-nx-1)]:
        wn, sow = time2gpst(time)
        print(f'Warning:GPS week = {wn:f} sow = {sow:.3f},chi-square test error! v={np.dot(v_,v_):.3f}')
        stat = 0
        return stat

    # validate GDOP
    GDOP = np.sqrt(Q[0, 0]+Q[1, 1]+Q[2, 2]+Q[3, 3])
    if GDOP > opt.maxgdop:
        wn, sow = time2gpst(time)
        print(f'Warning:GPS week = {wn:f} sow = {sow:.3f},GDOP test error! GDOP={GDOP:.3f}')
        stat = 0
        return stat
    
    return stat
