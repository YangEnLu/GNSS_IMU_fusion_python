from ...common.global_constants import glc, rtk, sat_t
import numpy as np
from .rescode import rescode
from ...common.leastsquare import least_square
from ...common.timeadd import timeadd
from .valsol import valsol
from ...common.time2gpst import time2gpst


def estpos(rtk: rtk, obs, nav, sv, opt):
    NX = 3 + glc().NSYS
    MAXITER = 10
    iter = 1
    time = obs[0, 0].time
    xr0 = np.transpose(rtk.sol.pos)
    xr0 = np.append(xr0, np.zeros((glc().NSYS, 1)), axis=0)

    while iter <= MAXITER:
        # compute residual,measurement model,weight matrix
        v, H, P, vsat, azel, resp, nv, ns = rescode(iter, obs, nav, sv, xr0, opt)
        sat_ = sat_t()
        sat_.vsat = vsat
        sat_.azel = azel
        sat_.resp = resp

        if nv < NX:
            stat = 0
            return rtk, sat_, Q, stat

        dx, Q, VAR = least_square(v, H, P, nv, ns)
        xr0 = xr0+dx
        iter = iter+1

        dx = np.reshape(dx, -1)
        if np.dot(dx, dx) < 1e-4:
            rtk.sol.time = timeadd(obs[0, 0].time, -xr0[3, 0]/glc().CLIGHT)
            rtk.sol.ns = ns
            rtk.sol.ratio = 0
            rtk.sol.pos = np.transpose(xr0[0:3,:])
            rtk.sol.vel = np.zeros((1, 3))
            rtk.sol.posP[0, 0] = VAR[0, 0]  # X
            rtk.sol.posP[0, 1] = VAR[1, 1]  # Y
            rtk.sol.posP[0, 2] = VAR[2, 2]  # Z
            rtk.sol.posP[0, 3] = VAR[0, 1]  # XY
            rtk.sol.posP[0, 4] = VAR[1, 2]  # YZ
            rtk.sol.posP[0, 5] = VAR[0, 2]  # XZ
            for i in range(int(np.shape(xr0)[0]-3)):
                rtk.sol.dtr[0, i] = xr0[3+i, 0]/glc().CLIGHT

            # validate solution
            # TODO need to check
            stat = valsol(time, v, P, vsat, Q, opt)
            if stat == 1:
                rtk.sol.stat = glc().SOLQ_SPP
                t = rtk.sol.time.time+rtk.sol.time.sec
                print(f'{t:.4f},{xr0[0,0]:.4f},{xr0[1,0]:.4f},{xr0[2,0]:.4f}')
                return rtk, sat_, Q, stat
            return rtk, sat_, Q, stat

    if iter > MAXITER:
        stat = 0
        week, sow = time2gpst(time)
        print(f'Warning:GPS week = {week:d} sow = {sow:.3f},SPP iteration divergent!')
        return rtk, sat_, Q, stat

    return rtk, sat_, Q, stat
