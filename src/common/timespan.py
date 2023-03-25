from .global_constants import rtk, obs, gtime
from .timediff import timediff
import numpy as np


def timespan(rtk: rtk, obsr: obs):
    conf_ts = rtk.opt.ts
    conf_te = rtk.opt.te
    obs_ts = gtime()
    obs_te = gtime()

    obs_ts.time = obsr.data[0, 0]
    obs_ts.sec = obsr.data[0, 1]
    obs_te.time = obsr.data[-1, 0]
    obs_te.sec = obsr.data[-1, 1]
    dt = obsr.dt

    if conf_ts.time != 0 and timediff(conf_ts, obs_ts) >= 0:
        ts = conf_ts
    else:
        ts = obs_ts

    if conf_te.time != 0 and timediff(conf_te, obs_te) <= 0:
        te = conf_te
    else:
        te = obs_te

    tspan = np.fix(timediff(te, ts)/dt)+1

    return tspan
