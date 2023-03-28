from ..common.timediff import timediff
from ..common.timeadd import timeadd
from ..common.global_constants import gtime


def adjweek(t1: gtime, t2: gtime):
    tt = timediff(t1,t2)
    if tt<-302400:
        t = timeadd(t1,604800)
        return t
    if tt>302400:
        t = timeadd(t1,-604800)
        return t
    
    t = gtime()
    t.time = t1.time
    t.sec = t1.sec
    return t
    
