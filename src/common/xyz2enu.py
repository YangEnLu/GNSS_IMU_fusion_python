import numpy as np


def xyz2enu(pos: np.ndarray) -> np.ndarray:

    sinp = np.sin(pos[0, 0])
    cosp = np.cos(pos[0, 0])
    sinl = np.sin(pos[1, 0])
    cosl = np.cos(pos[1, 0])

    E = np.array([[-sinl, cosl, 0.0],
                  [-sinp*cosl, -sinp * sinl, cosp],
                  [cosp*cosl, cosp*sinl, sinp]])

    return E
