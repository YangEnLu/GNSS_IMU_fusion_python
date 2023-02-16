from .global_constants import glc


def obs2code(obs, sys):
    obscodes = glc().obscodes

    if sys == glc().SYS_GPS:
        obsfreq = glc().GPSfreqband
    elif sys == glc().SYS_GLO:
        obsfreq = glc().GLOfreqband
    elif sys == glc().SYS_GAL:
        obsfreq = glc().GALfreqband
    elif sys == glc().SYS_BDS:
        obsfreq = glc().BDSfreqband
    elif sys == glc().SYS_QZS:
        obsfreq = glc().QZSfreqband

    code = 0
    frq = 0
    for i in range(1, 60):
        if not obscodes[i] == obs:
            continue
        frq = obsfreq[i]
        code = i+1
        break
    pass

    return code, frq
