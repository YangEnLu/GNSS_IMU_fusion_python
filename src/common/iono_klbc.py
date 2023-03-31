from .global_constants import glc, gtime
from .time2gpst import time2gpst
import numpy as np


def iono_klbc(time: gtime, pos, azel, ionpar):

    # 2004/1/1
    ion_default = [0.1118E-07, -0.7451E-08, -0.5961E-07,
                   0.1192E-06, 0.1167E+06, -0.2294E+06, -0.1311E+06, 0.1049E+07]
    azel = np.reshape(azel, (1, 2))
    pos = np.reshape(pos, (3, 1))

    if pos[2, 0] < -1e3 or azel[0, 1] <= 0:
        ion = 0
        return ion

    ionpar = np.reshape(ionpar, -1)
    if np.sqrt(np.dot(ionpar, ionpar)) <= 0:
        ionpar = np.array(ion_default).reshape((1, 8))

    azel = azel*180/np.pi
    ion = np.zeros((np.shape(azel)[0], 1))
    lat = pos[0, 0]*180/np.pi
    lon = pos[1, 0]*180/np.pi
    az = azel[0, 0]
    el = azel[0, 1]

    ionpar = np.reshape(ionpar, (1, 8))
    # ionospheric parameters
    a0 = ionpar[0, 0]
    a1 = ionpar[0, 1]
    a2 = ionpar[0, 2]
    a3 = ionpar[0, 3]
    b0 = ionpar[0, 4]
    b1 = ionpar[0, 5]
    b2 = ionpar[0, 6]
    b3 = ionpar[0, 7]

    # elevation from 0 to 90 degrees
    el = np.abs(el)

    # conversion to semicircles
    lat = lat / 180
    lon = lon / 180
    az = az / 180
    el = el / 180

    f = 1 + 16*(0.53-el)**3

    psi = (0.0137 / (el+0.11)) - 0.022

    phi = lat + psi * np.cos(az*np.pi)
    # phi[phi > 0.416] = 0.416
    # phi[phi < -0.416] = -0.416

    lambda_ = lon + ((psi*np.sin(az*np.pi)) / np.cos(phi*np.pi))

    ro = phi + 0.064*np.cos((lambda_-1.617)*np.pi)

    week, sow = time2gpst(time)
    t = lambda_*43200 + sow
    t = np.mod(t, 86400)

    a = a0 + a1*ro + a2*(ro**2) + a3*(ro**3)
    # a[a < 0] = 0

    p = b0 + b1*ro + b2*(ro**2) + b3*(ro**3)
    # p[p < 72000] = 72000

    x = (2*np.pi*(t-50400)) / p

    # ionospheric delay
    if np.abs(x) < 1.57:
        ion = glc().CLIGHT*f*(5e-9+a) * (1-(x**2)/2+(x**4)/24)
    else:
        ion = glc().CLIGHT * f * 5e-9

    return ion
