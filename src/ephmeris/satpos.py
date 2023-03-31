from ..common.global_constants import glc, gtime, nav, gls, sv, eph
from ..ephmeris.ephpos import ephpos


def satpos(time: gtime, obs, nav: nav, ephopt, sv: sv):

    teph = obs.time
    sat = obs.sat

    if ephopt == glc().EPHOPT_BRDC:
        sv_tmp = gls().sv
        sv_tmp.dts = sv.dts
        sv_tmp.dtsd = sv.dtsd
        sv_tmp.pos = sv.pos
        sv_tmp.svh = sv_tmp.svh
        sv_tmp.vars = sv_tmp.vars
        sv_tmp.vel = sv_tmp.vel
        sv, stat = ephpos(time, teph, sat, nav, -1, sv_tmp)
        return sv, stat
    elif ephopt == glc().EPHOPT_PREC:
        # TODO Finish PRECISE EPH
        pass
        return sv, stat
    else:
        stat = 0
        return sv, stat
