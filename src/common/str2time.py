from ..common.global_constants import gls
from ..common.epoch2time import epoch2time
import numpy as np

def str2time(str):
    time = gls().gtime
    ep = str.split()
    for i in range(len(ep)):
        ep[i]=float(ep[i])
    ep = np.array(ep)
    idx = (ep==np.NAN)
    if np.any(idx):
        return time
    
    if ep[0]<100:
        if ep[0]<80:
            ep[0]=ep[0]+2000
        else:
            ep[0]=ep[0]+1900
    
    time = epoch2time(ep)
    
    return time
    