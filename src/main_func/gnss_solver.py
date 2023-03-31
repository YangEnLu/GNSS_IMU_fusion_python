from ..common.global_constants import glc, rtk, nav
from ..gnss.spp.scan_obs_spp import scan_obs_spp
from ..gnss.spp.bds2mp_corr import bds2mp_corr
from ..gnss.spp.sppos import sppos
from ..common.timediff import timediff


def gnss_solver(rtk: rtk, obsr, obsb, nav: nav):

    time = rtk.sol.time
    opt = rtk.opt
    rtk.sol.stat = glc().SOLQ_NONE

    if opt.mode == glc().PMODE_SPP or opt.mode >= glc().PMODE_PPP_KINEMA:
        # scan obs for SPP
        obsr, nobs = scan_obs_spp(obsr)
        if nobs == 0:
            stat0 = 0
            return rtk, stat0
        # correct BDS2 multipath error
        if opt.navsys.find("C") != -1:
            obsr = bds2mp_corr(rtk, obsr)

    # standard point positioning
    rtk, stat0 = sppos(rtk, obsr, nav)
    if stat0 == 0:
        return rtk, stat0
    
    if time.time != 0:
        rtk.tt = timediff(rtk.sol.time,time)
    if opt.mode == glc().PMODE_SPP:
        return rtk, stat0
    
    # TODO PPP not done

    return rtk, stat0
