from .global_constants import gtime


def timediff(t1:gtime, t2:gtime):
    t = t1.time-t2.time+t1.sec-t2.sec
    return t
