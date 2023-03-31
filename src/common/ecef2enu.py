from .xyz2enu import xyz2enu
import numpy as np


def ecef2enu(pos,LOS):
    pos = np.reshape(pos,(3,1))
    E = xyz2enu(pos)
    enu = E @ np.transpose(LOS)
    
    return enu