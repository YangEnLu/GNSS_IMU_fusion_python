from .global_constants import glc, gtime, obs, gls, obs_tmp
import numpy as np
import numpy.matlib as npm


def searchobsb(obss: obs, time: gtime):

    obs = npm.repmat(obs_tmp(), glc().MAXOBS, 1)

    time0 = obss.data[:, 0]+obss.data[:, 1]
    time1 = time.time+time.sec

    idx = np.abs(time0-time1) <= glc().MAXAGE
    time_tmp = time0[idx]
    if not np.any(idx):
        obs = np.NaN
        nobs = 0
        return obs, nobs

    dt = np.abs(time_tmp-time1)
    mindt = np.min(dt)
    idx = (dt == mindt)
    if np.any(idx):
        mintime0 = time_tmp[idx]
        mintime = mintime0[0]
        idx = (time0 == mintime)
        obs0 = obss.data[idx, :]
        nobs = np.size(obs0, 0)
    else:
        obs = np.NaN
        nobs = 0
        return obs, nobs

    for i in range(nobs):
        obs[i, 0].time.time = obs0[i, 0]
        obs[i, 0].time.sec = obs0[i, 1]
        obs[i, 0].sat = obs0[i, 2]
        obs[i, 0].P = obs0[i, 3:6]
        obs[i, 0].L = obs0[6:9]
        obs[i, 0].D = obs0[9:12]
        obs[i, 0].S = obs0[12:15]
        obs[i, 0].LLI = obs0[15:18]
        obs[i, 0].code = obs0[18:21]
        
    obs = obs[0:nobs,]

    return obs, nobs
