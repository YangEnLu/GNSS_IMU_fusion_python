from ..common.global_constants import gtime, geph
from ..common.timediff import timediff


def geph2clk(time:gtime,geph:geph):
    
    t = timediff(time,geph.toe)
    for i in range(3):
        t = t-(-geph.taun+geph.gamn*t)
    
    dts = -geph.taun+geph.gamn*t
    
    return dts