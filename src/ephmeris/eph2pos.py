from ..common.global_constants import glc, eph, gtime, sv
from ..common.timediff import timediff
from ..common.satsys import satsys
from ..common.timediff import timediff
from .var_uraeph import var_uraeph
import numpy as np


def eph2pos(time: gtime, eph: eph, sv: sv):
    # calculate satellite position and velocity using broadcast ephemeris
    MU_GPS = 3.9860050e14     # gravitational constant
    MU_GAL = 3.986004418e14   # earth gravitational constant
    MU_BDS = 3.986004418e14   # earth gravitational constant
    OMGE_GAL = 7.2921151467e-5  # earth angular velocity (rad/s)
    OMGE_BDS = 7.292115e-5      # earth angular velocity (rad/s)
    RTOL_KEPLER = 1e-13
    MAX_ITER_KEPLER = 30
    SIN_5 = -0.0871557427476582  # sin(-5.0 deg)
    COS_5 = 0.9961946980917456  # cos(-5.0 deg)

    if eph.A <= 0:
        return sv

    tk = timediff(time, eph.toe)
    sys, prn = satsys(eph.sat)
    if sys == glc().SYS_GAL:
        mu = MU_GAL
        omge = OMGE_GAL
    elif sys == glc().SYS_BDS:
        mu = MU_BDS
        omge = OMGE_BDS
    else:
        mu = MU_GPS
        omge = glc().OMGE

    M = eph.M0 + (np.sqrt(mu/(eph.A**3)) + eph.deln)*tk

    n = 0
    E = M
    Ek = 0
    while np.abs(E-Ek) > RTOL_KEPLER and n < MAX_ITER_KEPLER:
        Ek = E
        E = E-(E-eph.e*np.sin(E)-M)/(1-eph.e*np.cos(E))
        n = n+1

    if n >= MAX_ITER_KEPLER:
        return sv
    sinE = np.sin(E)
    cosE = np.cos(E)

    u = np.arctan2((np.sqrt(1.0-eph.e*eph.e)*sinE),(cosE-eph.e))+eph.omg
    r = eph.A*(1.0-eph.e*cosE)
    i = eph.i0 + eph.idot*tk
    sin2u = np.sin(2*u)
    cos2u = np.cos(2*u)
    u = u+eph.cus*sin2u+eph.cuc*cos2u
    r = r+eph.crs*sin2u+eph.crc*cos2u
    i = i+eph.cis*sin2u+eph.cic*cos2u
    x = r*np.cos(u)
    y = r*np.sin(u)
    cosi = np.cos(i)

    if sys == glc().SYS_BDS and (eph.flag == 2 or (eph.flag == 0 and prn <= 5)):
        O = eph.OMG0 + eph.OMGd*tk - omge*eph.toes
        sinO = np.sin(O)
        cosO = np.cos(O)
        xg = x*cosO-y*cosi*sinO
        yg = x*sinO+y*cosi*cosO
        zg = y*np.sin(i)
        sino = np.sin(omge*tk)
        coso = np.cos(omge*tk)
        rs = np.array([[xg*coso+yg*sino*COS_5+zg*sino*SIN_5],
                       [-xg*sino+yg*coso*COS_5+zg*coso*SIN_5],
                       [-yg*SIN_5+zg*COS_5]])
    else:
        O = eph.OMG0+(eph.OMGd-omge)*tk-omge*eph.toes
        sinO = np.sin(O)
        cosO = np.cos(O)
        rs = np.array(
            [[x*cosO-y*cosi*sinO], [x*sinO+y*cosi*cosO], [y*np.sin(i)]])

    tk = timediff(time, eph.toc)
    dts = eph.f0+eph.f1*tk+eph.f2*tk*tk
    dts = dts - 2*np.sqrt(mu*eph.A)*eph.e*sinE/(glc().CLIGHT)**2
    vars = var_uraeph(sys,int(eph.sva+1))
    
    sv.pos = rs
    sv.dts = dts
    sv.vars = vars

    return sv
