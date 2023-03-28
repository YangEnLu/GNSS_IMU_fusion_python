from ..common.global_constants import gtime
from ..common.timediff import timediff
from ..common.timeadd import timeadd


def adjday(t1: gtime, t2: gtime):

    tt = timediff(t1, t2)

    if tt < -43200:
        t = timeadd(t1, 86400)
        return t

    if tt > 43200:
        t = timeadd(t1, -86400)
        return t
    
    t = gtime()
    t.time = t1.time
    t.sec = t1.sec
    return t
