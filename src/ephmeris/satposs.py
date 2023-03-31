from ..common.global_constants import glc, gls, sv, gtime
import numpy as np
import numpy.matlib as npm
from ..common.timeadd import timeadd
from .ephclk import ephclk
from .satpos import satpos


def satposs(obs, nav, ephopt):
    # compute satellite position,clock bias,velocity,clock drift
    # %
    # %input: obs   - observation
    # %       nav   - navigation message
    # %       ephopt- ephemeric option(0:using broadcast eph;1:using precise eph)
    # %output: sv   - space vehicle struct(record satellite position,clock bias,
    # %           velocity and clock drift)
    # %1.satellite position and clock are values at signal transmission time
    # %2.satellite position is referenced to antenna phase center
    # %3.satellite clock does not include code bias correction (tgd or bgd)
    # %4.any pseudorange and broadcast ephemeris are always needed to get signal
    # %  transmission time
    # %5.only surport broadcast/precise ephemeris,not RTCM-SSR

    STD_BRDCCLK = 30.0
    time0 = gtime()
    time0.time = obs[0, 0].time.time
    time0.sec = obs[0, 0].time.sec
    nobs = np.shape(obs)[0]
    sv_ = npm.repmat(sv(), nobs, 1)

    for i in range(nobs):
        for j in range(glc().NFREQ):
            pr = obs[i, 0].P[j, 0]
            if pr != 0:
                break
        if pr == 0:
            continue

        time = timeadd(time0, -pr/glc().CLIGHT)  # raw single transition time

        dts, stat1 = ephclk(time, obs[i, 0], nav)
        if stat1 == 0:
            continue

        time = timeadd(time, -dts)  # signal transition time

        sv_[i, 0], stat2 = satpos(time, obs[i, 0], nav, ephopt, sv_[i, 0])

        if stat2 == 0:
            continue

        if sv_[i, 0].dts == 0:
            dts, stat1 = ephclk(time, obs[i, 0], nav)
            if stat1 == 0:
                continue
            # sv_[i, 0].dtsd = dts
            sv_[i, 0].dtsd = 0
            sv_[i, 0].vars = STD_BRDCCLK ** 2

    return sv_
