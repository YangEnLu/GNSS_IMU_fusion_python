from .global_constants import glc, gtime, eph, gls
from .satsys import satsys
import numpy as np


def searcheph_h(time: gtime, sat, iode, eph: eph):
    # %search the corresponding navigation meassage with high efficiency
    eph_sel = [0, 0, 1, 0, 0]
    stat = 1
    sel = 0
    
    sys, prn = satsys(sat)

    if sys == glc().SYS_GPS:
        tmax = glc().MAXDTOE+1
        sel = eph_sel[0]
    elif sys == glc().SYS_GAL:
        tmax = glc().MAXDTOE_GAL
        sel = eph_sel[2]
    elif sys == glc().SYS_BDS:
        tmax = glc().MAXDTOE_BDS+1
        sel = eph_sel[3]
    elif sys == glc().SYS_QZS:
        tmax = glc().MAXDTOE_QZS+1
        sel = eph_sel[4]
    else:
        tmax = glc().MAXDTOE+1
    tmin = tmax + 1

    idx0 = eph[:, 0] == sat
    if not np.any(idx0):
        eph_out = np.NaN
        stat = 0
        return eph_out, stat
    eph0 = eph[idx0, :]
    if sys == glc().SYS_GAL and sel != 0:
        if sel == 1:
            idx_GAL = np.bitwise_and[eph0[:, 6], np.left_shift[1, 9]] != 0
            if not np.any[idx_GAL]:
                eph_out = np.NaN
                stat = 0
                return eph_out, stat
            eph0 = eph0[idx_GAL, :]
        if sel == 2:
            idx_GAL = np.bitwise_and[eph0[:, 6], np.left_shift[1, 8]] != 0
            if not np.any[idx_GAL]:
                eph_out = np.NaN
                stat = 0
                return eph_out, stat
            eph0 = eph0[idx_GAL, :]
    t0 = np.abs(eph0[:, 10]+eph0[:, 11]-time.time-time.sec)
    idx1 = (t0 <= tmax) & (t0 <= tmin)
    if not np.any(idx1):
        eph_out = np.NAN
        stat = 0
        return eph_out, stat
    t1 = t0[idx1]
    eph1 = eph0[idx1, :]
    idx2 = t1 == np.min(t1)
    eph_ = eph1[idx2, :]
    eph2 = np.reshape(eph_[-1, :],(1,-1))

    eph_out = gls().eph
    eph_out.sat = eph2[0, 0]
    eph_out.iode = eph2[0, 1]
    eph_out.iodc = eph2[0, 2]
    eph_out.sva = eph2[0, 3]
    eph_out.svh = eph2[0, 4]
    eph_out.week = eph2[0, 5]
    eph_out.code = eph2[0, 6]
    eph_out.flag = eph2[0, 7]
    eph_out.toc = gtime()
    eph_out.toc.time = eph2[0, 8]
    eph_out.toc.sec = eph2[0, 9]
    eph_out.toe = gtime()
    eph_out.toe.time = eph2[0, 10]
    eph_out.toe.sec = eph2[0, 11]
    eph_out.ttr = gtime()
    eph_out.ttr.time = eph2[0, 12]
    eph_out.ttr.sec = eph2[0, 13]
    eph_out.A = eph2[0, 14]
    eph_out.e = eph2[0, 15]
    eph_out.i0 = eph2[0, 16]
    eph_out.OMG0 = eph2[0, 17]
    eph_out.omg = eph2[0, 18]
    eph_out.M0 = eph2[0, 19]

    eph_out.deln = eph2[0, 20]
    eph_out.OMGd = eph2[0, 21]
    eph_out.idot = eph2[0, 22]
    eph_out.crc = eph2[0, 23]
    eph_out.crs = eph2[0, 24]
    eph_out.cuc = eph2[0, 25]
    eph_out.cus = eph2[0, 26]
    eph_out.cic = eph2[0, 27]
    eph_out.cis = eph2[0, 28]
    eph_out.toes = eph2[0, 29]

    eph_out.fit = eph2[0, 30]
    eph_out.f0 = eph2[0, 31]
    eph_out.f1 = eph2[0, 32]
    eph_out.f2 = eph2[0, 33]
    eph_out.tgd = eph2[0, 34:38]
    eph_out.Adot = eph2[0, 38]
    eph_out.ndot = eph2[0, 39]

    return eph_out, stat
