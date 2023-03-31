import numpy as np


def trop_saa(pos, azel, humi):
    # temperature
    temp0 = 15
    pos = np.reshape(pos, (1, 3))
    azel = np.reshape(azel, (1, 2))
    if pos[0, 2] < -100 or pos[0, 2] > 10000 or azel[0, 1] <= 0:
        troperr = 0
        return troperr

    # standard atmosphere
    if pos[0, 2] < 0:
        hgt = 0
    else:
        hgt = pos[0, 2]
    pres = 1013.25*(1.0-2.2557E-5*hgt)**5.2568
    temp = temp0-6.5E-3*hgt+273.16
    e = 6.108*humi*np.exp((17.15*temp-4684.0)/(temp-38.45))

    # saastamoninen model
    z = np.pi/2.0-azel[0, 1]
    trph = 0.0022768*pres / \
        (1.0-0.00266*np.cos(2.0*pos[0, 0])-0.00028*hgt/1E3)/np.cos(z)
    trpw = 0.002277*(1255.0/temp+0.05)*e/np.cos(z)

    # wet + dry
    troperr = trph+trpw

    return troperr
