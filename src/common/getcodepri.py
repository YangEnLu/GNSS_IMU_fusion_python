from .global_constants import glc
from .code2obs import code2obs
from ..readfile.find_str import find_str
import numpy as np

def getcodepri(sys,code,opt):
    
    codepris = glc().codepris
    
    if sys==glc().SYS_GPS:
        i=1
        optstr="-GL"
    elif sys==glc().SYS_GLO:
        i=2
        optstr="-RL"
    elif sys==glc().SYS_GAL:
        i=3
        optstr="-EL"
    elif sys==glc().SYS_BDS:
        i=4
        optstr="-BL"
    elif sys==glc().SYS_QZS:
        i=5
        optstr="-QL"
        
    pri = 0
    obs,j = code2obs(code,sys)
    if obs=="" or j==0:
        return pri
    
    ind=find_str(codepris[i-1,j-1],obs[1]) # i: sys, j: freq
    
    if np.any(np.array(ind[0]+1)):
        pri=15-(ind[0]+1)
    else:
        pri=0
        
    return pri  