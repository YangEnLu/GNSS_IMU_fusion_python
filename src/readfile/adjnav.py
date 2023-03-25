from ..common.global_constants import nav, default_opt, glc
from ..common.satsys import satsys
import numpy as np


def adjnav(nav: nav, opt: default_opt):

    # adjust eph
    if nav.n > 0:
        eph0 = np.zeros((nav.n, 40))
        for i in range(nav.n):
            eph = nav.eph[i, 0]
            eph0[i, 0:34] = [eph.sat, eph.iode, eph.iodc, eph.sva, eph.svh, eph.week, eph.code, eph.flag, eph.toc.time, eph.toc.sec,
                             eph.toe.time, eph.toe.sec, eph.ttr.time, eph.ttr.sec, eph.A, eph.e, eph.i0, eph.OMG0, eph.omg, eph.M0,
                             eph.deln, eph.OMGd, eph.idot, eph.crc, eph.crs, eph.cuc, eph.cus, eph.cic, eph.cis, eph.toes,
                             eph.fit, eph.f0, eph.f1, eph.f2]
            tgd = eph.tgd.tolist()[0]
            eph0[i, 34:38] = tgd
            eph0[i, 38] = eph.Adot
            eph0[i, 39] = eph.ndot
        del nav.eph
        nav.eph = eph0

    # adjust geph
    if nav.ng > 0:
        geph0 = np.zeros((nav.ng, 22))
        for i in range(nav.ng):
            geph = nav.geph[i, 0]
            geph0[i, 0:10] = [geph.sat, geph.iode, geph.frq, geph.svh, geph.sva,
                              geph.age, geph.toe.time, geph.toe.sec, geph.tof.time, geph.tof.sec]
            geph0[i, 10:13] = np.transpose(geph.pos).tolist()[0]
            geph0[i, 13:16] = np.transpose(geph.vel).tolist()[0]
            geph0[i, 16:19] = np.transpose(geph.acc).tolist()[0]
            geph0[i, 19] = geph.taun
            geph0[i, 20] = geph.gamn
            geph0[i, 21] = geph.dtaun

    # adjust wavelength
    bds_frq_flag = 1
    lam = nav.lam
    del nav.lam
    nav.lam = np.zeros((glc().MAXSAT, glc().NFREQ))
    if glc().NFREQ > 3 and (len(opt.bd2frq) <= 3 or len(opt.bd3frq) <= 3) and opt.navsys.find("C") != -1:
        bds_frq_flag = 0
        print("Warning:Specified frequency of BDS less than used number of frequency!")
    for i in range(glc().MAXSAT):
        sys, prn = satsys(i+1)
        if sys == glc().SYS_BDS:
            if prn <= 19:  # BD2
                if not bds_frq_flag:
                    continue
                frq = opt.bd2frq
                for j in range(glc().NFREQ):
                    nav.lam[i, j] = lam[i, int(frq[j])]
            else:  # BD3
                if not bds_frq_flag:
                    continue
                for j in range(glc().NFREQ):
                    nav.lam[i, j] = lam[i, int(frq[j])]
        else:  # GPS GLO GAL QZS
            nav.lam[i, ] = lam[i, 0:3]
    
    return nav
