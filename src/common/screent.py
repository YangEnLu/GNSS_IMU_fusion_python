from ..common.global_constants import glc, gtime
from ..common.str2time import str2time
from ..common.time2gpst import time2gpst
from ..common.timediff import timediff
import numpy as np


def screent(time: gtime, ts0: str, te0: str, ti):
    stat = 1
    ts = str2time(ts0)
    te = str2time(te0)
    week, sow = time2gpst(time)

    if ti > 0 and (sow+glc().DTTOL) % ti > (2*glc().DTTOL):
        stat = 0

    if ts.time != 0 and timediff(time, ts) < -glc().DTTOL:
        stat = 0

    if te.time != 0 and timediff(time, te) >= glc().DTTOL:
        stat = 0

    return stat
