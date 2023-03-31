from ..common.global_constants import gls,  obs_tmp
import numpy as np
import numpy.matlib as npm


def searchobsr(obss):
    if obss.idx >= obss.n:
        obs = np.NaN
        nobs = -1
        return obs, nobs, obss

    obss.idx = obss.idx + 1
    obs_tmp_ = obss.data[obss.idx-1, :]

    time0 = obss.data[:, 0]+obss.data[:, 1]
    time1 = obs_tmp_[0] + obs_tmp_[1]
    idx = (time0 == time1)
    pos = np.asarray(np.nonzero(idx)).reshape(-1)

    if any(idx):
        obs0 = obss.data[idx, :]
        nobs = np.size(obs0, 0)
        obss.idx = pos[-1]+1
    else:
        nobs = 0
        obs = np.NaN
        return obs, nobs, obss

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

    return obs, nobs, obss
