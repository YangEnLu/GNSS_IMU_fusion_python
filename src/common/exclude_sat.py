from .global_constants import rtk, gls, obs_tmp
import numpy as np
import numpy.matlib as npm
from ..readfile.set_sysmask import set_sysmask
from .timediff import timediff
from .satsys import satsys


def exclude_sat(obs0: np.ndarray, rtk: rtk):
    nobs0 = np.size(obs0, 0)
    nobs = 0
    obs = npm.repmat(obs_tmp(), nobs0, 1)
    ts = rtk.opt.ts
    te = rtk.opt.te
    mask = set_sysmask(rtk.opt.navsys)

    for i in range(nobs0):
        time = obs0[i, 0].time
        if ts.time != 0:
            dt = timediff(time, ts)
            if dt < 0:
                continue
        if te.time != 0:
            dt = timediff(time, te)
            if dt < 0:
                continue

        # if obs0(i).sat==4;continue;end
        sys, prn = satsys(obs0[i, 0].sat)
        if mask[sys-1] == 0:
            continue

        obs[nobs, 0] = obs0[i, 0]
        nobs = nobs + 1

    if nobs == 0:
        obs = np.NaN
        return obs, nobs
    if nobs < nobs0:
        obs = obs[0:nobs, ]

    return obs, nobs
