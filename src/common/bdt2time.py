from ..common.global_constants import gtime
from .epoch2time import epoch2time
import numpy as np


def bdt2time(week: int, sec: float):
    t = gtime()

    # beidou time reference
    bdt0 = [2006, 1, 1, 0, 0, 0]
    t0 = epoch2time(bdt0)

    if sec < -1e9 or sec > 1e9:
        sec = 0

    t.time = t0.time + week*7*86400 + np.fix(sec)
    t.sec = sec - np.fix(sec)

    return t
