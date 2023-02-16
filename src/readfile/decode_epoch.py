from ..common.global_constants import glc, gls
from ..common.str2time import str2time
import numpy as np


def decode_epoch(ver, line):
    time = gls().gtime
    sats = np.zeros(glc().MAXOBS)
    flag = 0
    # ver 2.0
    if ver <= 2.99:
        ns = float(line[29:32])  # number of obs
        if ns<=0:
            return time, ns, sats, flag
        flag = float(line[28]) # Epoch flag
        if flag>=3 and flag<=5:
            return time, ns, sats, flag
        time = str2time(line[0:26])
    else:
        ns = float(line[32:35]) # number of obs
        if ns <=0:
            return time, ns, sats, flag
        flag = float(line[31])
        if flag>=3 and flag<=5:
            return time, ns, sats, flag
        if line[0]!=">":
            return time, ns, sats, flag
        time = str2time(line[1:29])

    return time, ns, sats, flag
