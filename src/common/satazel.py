from .global_constants import glc
from .ecef2enu import ecef2enu
import numpy as np


def satazel(pos, LOS) -> np.ndarray:
    pos = np.reshape(pos,(1,3))
    az = 0
    el = np.pi/2
    azel = np.array([[az, el]])
    pos = np.reshape(pos,(1,3))

    if pos[0, 2] > -glc().RE_WGS84:
        enu = ecef2enu(pos, LOS)
        if np.dot(enu.reshape(-1), enu.reshape(-1)) < 1e-12:
            az = 0
        else:
            az = np.arctan2(enu[0,0],enu[1,0])
        if az < 0:
            az = az + 2*np.pi
        el = np.arcsin(enu[2,0])
        
    azel = np.array([[az, el]])

    return azel
