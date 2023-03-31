from ...common.global_constants import glc, nav, obsd, default_opt
from ...common.satsys import satsys
from ...common.getdcb import getdcb
from .gettgd import gettgd


def prange(obs: obsd, nav: nav, opt: default_opt, azel, iter):

    lam = nav.lam[int(obs.sat-1), :]
    PC = 0
    Vmea = 0
    i = 0
    j = 1

    sys, prn = satsys(obs.sat)
    if sys == 0:
        return PC, Vmea

    if glc().NFREQ < 2 or lam[i] == 0 or lam[j] == 0:
        return PC, Vmea

    # TODO test snr mask
    # if iter>1:
    #     pass

    # pseudorange with code bias correction
    cbias, use_dcb_flag = getdcb(nav, obs, opt)
    if use_dcb_flag == 0 and sys != glc().SYS_GLO:
        cbias = gettgd(nav, obs, opt)
    P1 = obs.P[i, 0]-cbias[0, 0]
    P2 = obs.P[j, 0]-cbias[1, 0]

    gamma = lam[j]**2/lam[i]**2
    if opt.ionoopt == glc().IONOOPT_IFLC:
        if P1 == 0 or P2 == 0:
            return PC, Vmea
        PC = (gamma*P1-P2)/(gamma-1)
    else:
        if P1 == 0:
            return PC, Vmea
        PC = P1

    Vmea = 0.3**2

    return PC, Vmea
