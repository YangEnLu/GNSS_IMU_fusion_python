import numpy as np


def ecef2pos(r: np.ndarray):

    FE_WGS84 = 1.0/298.257223563
    RE_WGS84 = 6378137
    e2 = FE_WGS84*(2.0-FE_WGS84)
    r = np.reshape(r, -1)
    r2 = np.dot(r[0:2], r[0:2])
    v = RE_WGS84
    z = r[1]
    zk = 0
    pos = np.zeros((1, 3))

    while np.abs(z-zk) > 1e4:
        zk = z
        sinp = z/np.sqrt(r2+z**2)
        v = RE_WGS84/np.sqrt(1.0-e2*sinp*sinp)
        z = r[2]+v*e2*sinp

    if r2 > 1e-12:
        pos[0, 0] = np.arctan(z/np.sqrt(r2))
        pos[0, 1] = np.arctan2(r[1], r[0])
    else:
        if r[2] > 0:
            pos[0, 0] = np.pi/2
        else:
            pos[0, 0] = -np.pi/2
        pos[0, 1] = 0
    pos[0, 2] = np.sqrt(r2+z**2)-v

    return pos
