from .global_constants import glc, nav
from .iono_klbc import iono_klbc


def iono_cor(opt, time, nav: nav, sat, pos, azel):
    ERR_ION = 5.0

    if opt == glc().IONOOPT_OFF:
        iono_err = 0
        iono_var = ERR_ION**2
    elif opt == glc().IONOOPT_BRDC:  # broadcast ionosphere parameter+klobuchar model
        iono_err = iono_klbc(time, pos, azel, nav.ion_gps)
        iono_var = (0.5*iono_err)**2
    else:
        print("ERROR<iono_corr>: SPP not surpport this ionospheric correction option!!!")

    return iono_err, iono_var
