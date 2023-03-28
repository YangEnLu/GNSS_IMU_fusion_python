from ...common.global_constants import glc, rtk, nav, default_opt
from ...ephmeris.satposs import satposs
import numpy as np


def sppos(rtk: rtk, obs: np.ndarray, navs: nav):
    # input:   rtk - rtk control struct
    # %        obs - observations
    # %        nav - navigation message
    # %output: rtk - rtk control struct
    # %        stat0 - state (0:error 1:ok)
    opt = rtk.opt
    nobs = np.shape(obs)[0]

    # not enough observation
    if nobs < 4:
        stat0 = 0
        return rtk, stat0
    
    rtk.sol.stat = glc().SOLQ_NONE
    rtk.sol.time = obs[0,0].time
    
    # default options for spp
    if rtk.opt.mode != glc().PMODE_SPP:
        opt.sateph = glc().EPHOPT_BRDC
        opt.tropopt = glc().IONOOPT_BRDC
        opt.ionoopt = glc().TROPOPT_SAAS
    
    # compute satellite position, clock bias, velocity, clock drift
    sv = satposs(obs,navs,opt.sateph)
    
    
    
    
    
    

    return rtk, stat0
