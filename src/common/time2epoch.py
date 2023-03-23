from ..common.global_constants import gtime
import numpy as np


def time2epoch(t: gtime):
    ep = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31,
            31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    days = np.fix(t.time/86400)
    sec = np.fix(t.time-days*86400)
    day = days % 1461
    mon = 0

    while mon < 48:
        if day >= mday[mon+1]:
            day = day-mday[mon+1]
        else:
            break
        mon = mon + 1

    ep[0] = 1970+np.fix(days/1461)*4+np.fix(mon/12)
    ep[1] = mon % 12+1
    ep[2] = day+1
    ep[3] = np.fix(sec/3600)
    ep[4] = np.fix((sec % 3600)/60)
    ep[5] = (sec % 60)+t.sec

    return ep
