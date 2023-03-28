from ...common.global_constants import glc, gls, obs_tmp
import numpy as np
import numpy.matlib as npm


def scan_obs_spp(obsr):
    nobs0 = np.shape(obsr)[0]
    nobs = 0
    obs = npm.repmat(obs_tmp(), nobs0, 1)

    for i in range(nobs0):
        dt = 0
        for f in range(glc().NFREQ):
            dt = dt+obsr[i, 0].P[f, 0]*obsr[i, 0].P[f, 0]
        if dt == 0:
            continue
        obs[nobs, 0] = obsr[i, 0]
        nobs = nobs+1

    if nobs == 0:
        obs = np.NaN
        return obs, nobs

    if nobs < nobs0:
        obs = obs[0:nobs, ]

    return obs, nobs
