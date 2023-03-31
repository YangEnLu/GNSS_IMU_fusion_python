from ...common.global_constants import glc, default_opt, nav
from ...common.ecef2pos import ecef2pos
from ...common.satsys import satsys
from ...common.geodist import geodist
from ...common.satazel import satazel
from .prange import prange
from ...common.satexclude import satexclude
from ...common.iono_cor import iono_cor
from ...common.trop_cor import trop_cor
from .varerr_spp import varerr_spp

import numpy as np


def rescode(iter, obs, nav: nav, sv, x0, opt: default_opt):
    lam_carr0 = glc().CLIGHT/glc().FREQ_GPS_L1
    nobs = np.shape(obs)[0]
    NSYS = glc().NSYS
    v = np.zeros((nobs+NSYS, 1))
    H = np.zeros((nobs+NSYS, 8))
    P = np.zeros((nobs+NSYS, nobs+NSYS))
    vsat = np.zeros((nobs, 1))
    azel = np.zeros((nobs, 2))
    resp = np.zeros((nobs, 1))
    nv = 0
    ns = 0
    var = np.zeros((nobs+NSYS, nobs+NSYS))
    mask = np.zeros((5, 1))
    idx = np.zeros((nobs, 1))
    rr = np.reshape(x0[0:3, 0],(-1,1))
    dtr = x0[3, 0]
    pos = ecef2pos(rr)

    for i in range(nobs):
        vsat[i, 0] = 0
        azel[i, :] = np.array([0, 0])
        resp[i, 0] = 0

        sys, prn = satsys(obs[i, 0].sat)
        if sys == 0:
            continue
        
        if i == nobs-1:
            pass
        else:
            if i < nobs and obs[i, 0].sat == obs[i+1, 0].sat:
                continue

        rs = sv[i, 0].pos
        dts = sv[i, 0].dts
        Vars = sv[i, 0].vars

        r, LOS = geodist(rs, rr)
        azel[i, :] = satazel(pos, LOS)
        if r <= 0 or azel[i, 1] < opt.elmin:
            continue

        # pesudorange with code bias correction
        pr, Vmea = prange(obs[i, 0], nav, opt, azel[i, :], iter)
        if pr == 0:
            continue
        if np.abs(pr) < 1e7 or np.abs(pr) > 5e7:
            print("<rescode>: Weird pseudorange")
            continue

        # exclude satellite
        stat = satexclude(obs[i, 0].sat, Vars, sv[i, 0].svh, opt)
        if stat == 0:
            continue

        # ionospheric delay
        ionoerr, Viono = iono_cor(
            glc().IONOOPT_BRDC, obs[i, 0].time, nav, obs[i, 0].sat, pos, azel[i, :])
        lam_L1 = nav.lam[int(obs[i, 0].sat-1), 0]
        if lam_L1 > 0:
            ionoerr = ionoerr*(lam_L1/lam_carr0)**2

        # tropospheric delay
        troperr, Vtrop = trop_cor(
            glc().TROPOPT_SAAS, obs[i, 0].time, nav, pos, azel[i, :])

        # pseudorange residuals
        v[nv, 0] = pr - (r+dtr-glc().CLIGHT*dts+ionoerr+troperr)

        # design matrix
        H[nv, :] = np.concatenate((-LOS,np.array([[1,0,0,0,0]])),axis=1)
        if sys == glc().SYS_GLO:
            v[nv] = v[nv]-x0[4, 0]
            H[nv, 4] = 1
            mask[1, 0] = 1
        elif sys == glc().SYS_GAL:
            v[nv] = v[nv]-x0[5, 0]
            H[nv, 5] = 1
            mask[2, 0] = 1
        elif sys == glc().SYS_BDS:
            v[nv] = v[nv]-x0[6, 0]
            H[nv, 6] = 1
            mask[3, 0] = 1
        elif sys == glc().SYS_QZS:
            v[nv] = v[nv]-x0[7, 0]
            H[nv, 7] = 1
            mask[4, 0] = 1
        else:
            mask[0, 0] = 1

        # variance matrix
        VARr = varerr_spp(opt, azel[i, 1], sys)
        var[nv, nv] = VARr+Vars+Viono+Vtrop+Vmea

        # record validate satellite residual
        vsat[i, 0] = 1
        resp[i, 0] = v[nv, 0]
        idx[nv, 0] = i

        nv = nv+1
        ns = ns+1

    # add the virtual observation value to avoid rank defect
    for i in range(5):
        if mask[i, 0] == 1:
            continue
        v[nv, 0] = 0
        H[nv, 3+i] = 1
        var[nv, nv] = 0.01
        nv = nv+1

    # weight matrix
    for i in range(nv):
        P[i, i] = var[i, i]**-1

    if nv < nobs+NSYS:
        v = v[0:nv, :]
        H = H[0:nv, :]
        P = P[0:nv, 0:nv]
    
    return v,H,P,vsat,azel,resp,nv,ns
