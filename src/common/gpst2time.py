from ..common.global_constants import gtime
from .epoch2time import epoch2time
import numpy as np


def gpst2time(week,sec):
    t = gtime()
    gpst0 = [1980,1,6,0,0,0]
    
    t0 = epoch2time(gpst0)
    
    if sec<-1e9 or sec > 1e9:
        sec = 0
    
    t.time = t0.time + week*7*86400 + np.fix(sec)
    t.sec = sec - np.fix(sec)
    
    
    return t