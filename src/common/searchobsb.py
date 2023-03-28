from .global_constants import glc, gtime, obs, gls, obs_tmp
import numpy as np
import numpy.matlib as npm


def searchobsb(obss: obs, time: gtime):

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

    obs = npm.repmat(obs_tmp(), nobs, 1)
    for i in range(nobs):
        obs_t = obs_tmp()
        obs_t.time.time = obs0[i, 0]
        obs_t.time.sec = obs0[i, 1]
        obs_t.sat = obs0[i, 2]
        obs_t.P = np.reshape(obs0[i, 3:6], (3, 1))
        obs_t.L = np.reshape(obs0[i, 6:9], (3, 1))
        obs_t.D = np.reshape(obs0[i, 9:12], (3, 1))
        obs_t.S = np.reshape(obs0[i, 12:15], (3, 1))
        obs_t.LLI = np.reshape(obs0[i, 15:18], (3, 1))
        obs_t.code = np.reshape(obs0[i, 18:21], (3, 1))
        obs[i, 0] = obs_t

    obs = obs[0:nobs, ]

    return obs, nobs
