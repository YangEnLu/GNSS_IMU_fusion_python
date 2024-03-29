from .global_constants import glc


def satsys(sat):
    sys = 0
    if sat <= 0 or sat > glc().MAXSAT:
        sat = 0
    elif sat <= glc().NSATGPS:
        sys = glc().SYS_GPS
        sat = sat + glc().MINPRNGPS-1
    elif (sat-glc().NSATGPS) <= glc().NSATGLO:
        sys = glc().SYS_GLO
        sat = (sat-glc().NSATGPS)+glc().MINPRNGLO-1
    elif (sat-glc().NSATGPS-glc().NSATGLO) <= glc().NSATGAL:
        sys = glc().SYS_GAL
        sat = (sat-glc().NSATGPS-glc().NSATGLO)+glc().MINPRNGAL-1
    elif (sat-glc().NSATGPS-glc().NSATGLO-glc().NSATGAL) <= glc().NSATBDS:
        sys = glc().SYS_BDS
        sat = (sat-glc().NSATGPS-glc().NSATGLO-glc().NSATGAL)+glc().MINPRNBDS-1
    elif (sat-glc().NSATGPS-glc().NSATGLO-glc().NSATGAL-glc().NSATBDS) <= glc().NSATQZS:
        sys = glc().SYS_QZS
        sat = (sat-glc().NSATGPS-glc().NSATGLO -
               glc().NSATGAL-glc().NSATBDS)+glc().MINPRNQZS-1
    else:
        sat = 0

    prn = sat
    return sys, prn
