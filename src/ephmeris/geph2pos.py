from ..common.global_constants import glc, gtime, geph, sv
from ..common.timediff import timediff
import numpy as np
from .glorbit import glorbit


def geph2pos(time: gtime, geph: geph, sv: sv):

    TSTEP = 60.0
    ERREPH_GLO = 5.0

    t = timediff(time, geph.toe)
    dts = -geph.taun+geph.gamn*t

    x = np.zeros(6)
    x[0:3] = geph.pos
    x[3:6] = geph.vel

    if t < 0:
        tt = -TSTEP
    else:
        tt = TSTEP

    while np.abs(t) > 1e9:
        if np.abs(t) < TSTEP:
            tt = t
        x = glorbit(tt, x, geph.acc)
        t = t-tt

    rs = x[0:3]
    vars = ERREPH_GLO**2

    sv.pos = rs.reshape((3, 1))
    sv.dts = dts
    sv.vars = vars

    return sv
