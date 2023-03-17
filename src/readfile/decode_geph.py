from ..common.global_constants import glc, gls, gtime
from ..common.satsys import satsys
from ..common.time2gpst import time2gpst
from ..common.gpst2time import gpst2time
from ..common.utc2gpst import utc2gpst
from .adjday import adjday
import numpy as np
import math


def decode_geph(ver, sat, toc: gtime, data):
    geph = gls().geph
    stat = 1

    sys, prn = satsys(sat)
    if sys != glc().SYS_GLO:
        stat = 0
        return geph, stat

    geph.sat = sat

    # toc rounded by 15 min in utc
    week, tow = time2gpst(toc)
    toc = gpst2time(week, math.floor((tow+450)/900)*900)
    dow = np.fix(math.floor(tow/86400))

    # time of frame in utc
    if ver <= 2.99:
        tod = data[0, 2]
    else:
        tod = data[0, 2] % 86400
    tof = gpst2time(week, tod+dow*86400)
    tof = adjday(tof, toc)

    geph.toe = utc2gpst(toc)
    geph.tof = utc2gpst(tof)

    geph.iode = np.fix(((tow+10800) % 86400)/900+0.5)
    geph.taun = -data[0, 0]
    geph.gamn = data[0, 1]

    geph.pos = np.array([[data[0, 3]], [data[0, 7]], [data[0, 11]]])*1e3
    geph.vel = np.array([[data[0, 4]], [data[0, 8]], [data[0, 12]]])*1e3
    geph.acc = np.array([[data[0, 5]], [data[0, 9]], [data[0, 12]]])*1e3

    geph.svh = np.fix(data[0, 6])
    geph.frq = np.fix(data[0, 10])
    geph.age = np.fix(data[0, 14])

    # some receiver output >128 for minus frequency number
    if geph.frq > 128:
        geph.frq = geph.frq - 256

    return geph, stat
