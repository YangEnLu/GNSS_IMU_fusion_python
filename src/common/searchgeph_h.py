from .global_constants import gtime, geph, glc, gls
import numpy as np


def searchgeph_h(time: gtime, sat, iode, geph: geph):
    stat = 1
    tmax = glc().MAXDTOE_GLO
    tmin = tmax + 1

    idx0 = geph[:, 0] == sat
    if not np.any(idx0):
        geph_out = np.NaN
        stat = 0
        return geph_out, stat
    geph0 = geph[idx0, :]
    t0 = np.abs(geph0[:, 6]+geph0[:, 7]-time.time-time.sec)
    idx1 = (t0 <= tmax) & (t0 <= tmin)
    if not np.any(idx1):
        geph_out = np.NaN
        stat = 0
        return geph_out, stat
    t1 = t0[idx1]
    geph1 = geph0[idx1, :]
    idx2 = t1 == np.min(t1)
    geph_ = geph1[idx2, :]
    geph2 = np.reshape(geph_[-1, :], (1, -1))

    geph_out = gls().geph
    geph_out.sat = geph2[0, 0]
    geph_out.iode = geph2[0, 1]
    geph_out.frq = geph2[0, 2]
    geph_out.svh = geph2[0, 3]
    geph_out.sva = geph2[0, 4]
    geph_out.age = geph2[0, 5]
    geph_out.toe = gtime()
    geph_out.toe.time = geph2[0, 6]
    geph_out.toe.sec = geph2[0, 7]
    geph_out.tof = gtime()
    geph_out.tof.time = geph2[0, 8]
    geph_out.tof.sec = geph2[0, 9]

    geph_out.pos = np.reshape(geph2[0, 10:13], (3, 1))
    geph_out.vel = np.reshape(geph2[0, 13:16], (3, 1))
    geph_out.acc = np.reshape(geph2[0, 16:19], (3, 1))
    geph_out.taun = geph2[0, 19]

    geph_out.gamn = geph2[0, 20]
    geph_out.dtaun = geph2[0, 21]

    return geph_out, stat
