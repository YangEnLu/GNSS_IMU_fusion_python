from .global_constants import glc

def satno(sys,prn):
    sats = 0
    if prn<=0:
        return sats
    
    if sys==glc().SYS_GPS:
        if prn<glc().MINPRNGPS or glc().MAXPRNGPS<prn:
            return sats
        sats = prn - glc().MINPRNGPS+1
    elif sys==glc().SYS_GLO:
        if prn<glc().MINPRNGLO or glc().MAXPRNGLO<prn:
            return sats
        sats = glc().NSATGPS+prn-glc().MINPRNGLO+1
    elif sys==glc().SYS_GAL:
        if prn<glc().MINPRNGAL or glc().MAXPRNGAL<prn:
            return sats
        sats = glc().NSATGPS+glc().NSATGLO+prn-glc().MINPRNGAL+1
    elif sys==glc().SYS_BDS:
        if prn<glc().MINPRNBDS or glc().MAXPRNBDS<prn:
            return sats
        sats = glc().NSATGPS+glc().NSATGLO+glc().NSATGAL+prn-glc().MINPRNBDS+1
    elif sys==glc().SYS_QZS:
        if prn<glc().MINPRNQZS or glc().MAXPRNQZS<prn:
            return sats
        sats = glc().NSATGPS+glc().NSATGLO+glc().NSATGAL+glc().NSATBDS+prn-glc().MINPRNQZS+1
    
    return sats
        
    