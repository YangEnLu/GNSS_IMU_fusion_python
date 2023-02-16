from .global_constants import glc


def code2obs(code, sys):
    obscodes = glc().obscodes

    if sys == glc().SYS_GPS:
        obsfreqs = glc().GPSfreqband
    elif sys == glc().SYS_GLO:
        obsfreqs = glc().GLOfreqband
    elif sys == glc().SYS_GAL:
        obsfreqs = glc().GALfreqband
    elif sys == glc().SYS_BDS:
        obsfreqs = glc().BDSfreqband
    elif sys == glc().SYS_QZS:
        obsfreqs = glc().QZSfreqband

    if code <= 1 or glc().MAXCODE < code:
        obs = ""
        frq = 0
        return obs, frq

    obs = obscodes[int(code)-1]
    frq = obsfreqs[int(code)-1]

    return obs, frq
