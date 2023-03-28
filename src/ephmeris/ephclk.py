from ..common.global_constants import glc
from ..common.satsys import satsys
from ..common.searcheph_h import searcheph_h
from .eph2clk import eph2clk


def ephclk(time, obs, nav):
    dts = 0
    stat0 = 1

    teph = obs.time
    sat = obs.sat
    sys, prn = satsys(sat)

    if sys == glc().SYS_GPS or sys == glc().SYS_GAL or sys == glc().SYS_BDS or sys == glc().SYS_QZS:
        eph, stat = searcheph_h(teph, sat, -1, nav.eph)
        if stat == 0:
            stat0 = 0
            return dts, stat0
        dts = eph2clk(time, eph)
    elif sys == glc().SYS_GLO:
        pass

    return dts, stat0
