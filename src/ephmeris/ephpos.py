from ..common.global_constants import glc, sv, gls
from ..common.satsys import satsys
from ..common.searcheph_h import searcheph_h
from ..common.searchgeph_h import searchgeph_h
from .eph2pos import eph2pos
from .geph2pos import geph2pos
from ..common.timeadd import timeadd


def ephpos(time, teph, sat, nav, iode, sv: sv):
    stat0 = 1
    tt = 1e-3
    sv1 = gls().sv
    sys, prn = satsys(sat)

    if sys == glc().SYS_GPS or sys == glc().SYS_GAL or sys == glc().SYS_BDS or sys == glc().SYS_QZS:
        eph, stat = searcheph_h(teph, sat, -1, nav.eph)
        if stat == 0:
            stat0 = 0
            return sv, stat0
        sv = eph2pos(time, eph, sv)
        time = timeadd(time, tt)
        sv1 = eph2pos(time, eph, sv1)
        sv.svh = eph.svh
    elif sys == glc().SYS_GLO:
        geph, stat = searchgeph_h(teph, sat, -1, nav.geph)
        if stat == 0:
            stat0 = 0
            return sv, stat0
        sv = geph2pos(time,geph,sv)
        time = timeadd(time, tt)
        sv1 = geph2pos(time,geph,sv1)
        sv.svh = geph.svh
    else:
        stat0 = 0
        return sv, stat0

    sv.vel = (sv1.pos-sv.pos)/tt
    sv.dtsd = (sv1.dts-sv.dts)/tt
    
    return sv, stat0
