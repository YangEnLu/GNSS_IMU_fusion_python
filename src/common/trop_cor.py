from .global_constants import glc, default_opt, gtime, nav
from .trop_saa import trop_saa
import numpy as np


def trop_cor(opt, time: gtime, nav: nav, pos, azel):
    ERR_TROP = 3.0

    if opt == glc().TROPOPT_OFF:
        trop_err = 0
        trop_var = ERR_TROP**2
    elif opt == glc().TROPOPT_SAAS:  # Saastamoinen model
        trop_err = trop_saa(pos, azel, 0.7)  # humid = 0.7
        trop_var = (0.3/(np.sin(azel[1])+0.1))**2
    else:
        print("ERROR<trop_cor>: SPP not surpport this tropspheric correction option!!!")

    return trop_err, trop_var
