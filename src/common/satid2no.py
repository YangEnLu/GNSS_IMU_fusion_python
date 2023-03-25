from .global_constants import glc
from .satno import satno
from scanf import scanf


def satid2no(satid: str):
    sats = 0
    if len(satid) == 2:
        code, prn = scanf("%s%d", satid)
    elif len(satid) == 3:
        code = satid[0]
        prn = int(satid[1:3])
    else:
        print("Error in satid2no function")

    if code == "G":
        sys = glc().SYS_GPS
        prn = prn+glc().MINPRNGPS-1
    elif code == "R":
        sys = glc().SYS_GLO
        prn = prn+glc().MINPRNGLO-1
    elif code == "E":
        sys = glc().SYS_GAL
        prn = prn+glc().MINPRNGAL-1
    elif code == "C":
        sys = glc().SYS_BDS
        prn = prn+glc().MINPRNBDS-1
    elif code == "J":
        sys = glc().SYS_QZS
        prn = prn+glc().MINPRNQZS-1
    else:
        return sats

    sats = satno(sys, prn)
    return sats
