from ..common.global_constants import gtime
from .timeadd import timeadd


def bdt2gpst(t0: gtime):
    t = timeadd(t0, 14)
    return t
