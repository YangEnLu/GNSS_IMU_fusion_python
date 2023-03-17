from ..common.global_constants import glc, gls
from ..common.satsys import satsys
from .adjweek import adjweek
from ..common.gpst2time import gpst2time
from ..common.bdt2gpst import bdt2gpst
from .uraindex import uraindex
from .sisa_index import sisa_index
import numpy as np


def decode_eph(ver, sat, toc, data: np.ndarray):
    eph = gls().eph
    stat = 1
    sys, prn = satsys(sat)

    if sys != glc().SYS_GPS and sys != glc().SYS_GAL and sys != glc().SYS_BDS and sys != glc().SYS_QZS:
        stat = 0

    eph.sat = sat
    eph.toc = toc

    # 3 satellite clock  parameter
    eph.f0 = data[0, 0]
    eph.f1 = data[0, 1]
    eph.f2 = data[0, 2]

    # 15 satellite orbit parameter
    eph.A = data[0, 10]**2
    eph.e = data[0, 8]
    eph.i0 = data[0, 15]
    eph.OMG0 = data[0, 13]
    eph.omg = data[0, 17]
    eph.M0 = data[0, 6]
    eph.deln = data[0, 5]
    eph.OMGd = data[0, 18]
    eph.idot = data[0, 19]
    eph.crc = data[0, 16]
    eph.crs = data[0, 4]
    eph.cuc = data[0, 7]
    eph.cus = data[0, 9]
    eph.cic = data[0, 12]
    eph.cis = data[0, 14]

    if sys == glc().SYS_GPS or sys == glc().SYS_QZS:
        eph.iode = np.fix(data[0, 3])
        eph.iodc = np.fix(data[0, 26])
        eph.toes = data[0, 11]
        eph.week = np.fix(data[0, 21])
        eph.toe = adjweek(gpst2time(eph.week, data[0, 11]), toc)
        eph.ttr = adjweek(gpst2time(eph.week, data[0, 27]), toc)

        eph.code = np.fix(data[0, 20])
        eph.svh = np.fix(data[0, 24])
        eph.sva = uraindex(data[0, 23])
        eph.flag = np.fix(data[0, 22])

        eph.tgd[0, 0] = data[0, 25]
        if sys == glc().SYS_GPS:
            eph.fit = data[0, 28]
        else:
            if data[0, 28] == 0:
                eph.fit = 1
            else:
                eph.fit = 2

    elif sys == glc().SYS_GAL:  # GAL ver.3
        eph.iode = np.fix(data[0, 3])
        eph.toes = data[0, 11]
        eph.week = np.fix(data[0, 21])
        eph.toe = adjweek(gpst2time(eph.week, data[0, 11]), toc)
        eph.ttr = adjweek(gpst2time(eph.week, data[0, 27]), toc)

        eph.code = np.fix(data[0, 20])
        eph.svh = np.fix(data[0, 24])
        eph.sva = sisa_index(data[0, 23])

        eph.tgd[0, 0] = data[0, 25]
        eph.tgd[0, 1] = data[0, 26]
        
    elif sys == glc().SYS_BDS: #BDS ver.3.02
        eph.toc = bdt2gpst(eph.toc)
        

    return eph, stat
