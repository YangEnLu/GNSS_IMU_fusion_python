from ..common.timediff import timediff
from ..common.global_constants import gtime, eph


def eph2clk(time: gtime, eph: eph):

    t = timediff(time, eph.toc)
    for i in range(3):
        t = t - (eph.f0+eph.f1*t+eph.f2*t*t)
        
    t = eph.f0 + eph.f1*t + eph.f2*(t**2)
    
    return t
