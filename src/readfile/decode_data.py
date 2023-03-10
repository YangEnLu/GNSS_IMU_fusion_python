from ..common.global_constants import glc
from ..common.satid2no import satid2no
from ..common.satsys import satsys
import numpy as np


def is_float(element: any) -> bool:
    # If you expect None to be passed:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def decode_data(line, ver, data, mask, ind):
    stat = 1
    val = np.zeros(glc().MAXOBSTYPE)
    lli = np.zeros(glc().MAXOBSTYPE)
    p = np.full(glc().MAXOBSTYPE, np.nan)
    k = np.full(16, np.nan)
    l = np.full(16, np.nan)
    line = line[0:glc().MAXRNXLEN]
    if ver > 2.99:
        satid = line[0:3]
        data.sat = satid2no(satid)
    if data.sat == 0:
        stat = 0

    sys, prn = satsys(data.sat)
    if sys == 0:
        stat = 0
        return data, stat
    if mask[sys-1] == 0:
        stat = 0

    if sys == glc().SYS_GPS:
        ind_t = ind[0, sys-1]
    elif sys == glc().SYS_GLO:
        ind_t = ind[0, sys-1]
    elif sys == glc().SYS_GAL:
        ind_t = ind[0, sys-1]
    elif sys == glc().SYS_BDS:
        ind_t = ind[0, sys-1]
    elif sys == glc().SYS_QZS:
        ind_t = ind[0, sys-1]

    if ver <= 2.99:
        j = 0
    else:
        j = 3

    for i in range(ind_t.n):
        if ver <= 2.99 and j >= 80:
            line = line[0:glc().MAXRNXLEN]
            j = 0

        if j+15 > len(line):
            j = j+16
            continue

        if stat == 1:
            VAL = line[j:j+14]
            if is_float(VAL):
                VAL = float(VAL)
            else:
                VAL = np.nan
            if not np.isnan(VAL):
                val[i] = float(line[j:j+14])+ind_t.shift[0, i]

            LLI = line[j+14]
            if is_float(LLI):
                LLI = float(LLI)
            else:
                LLI = np.nan
            if not np.isnan(LLI):
                lli[i] = int(LLI) & 3
        j = j+16

    if stat == 0:
        return data, stat

    for i in range(glc().MAXFREQ):
        data.P[i, 0] = 0
        data.L[i, 0] = 0
        data.D[i, 0] = 0
        data.S[i, 0] = 0
        data.LLI[i, 0] = 0
        data.code[i, 0] = 0

    n = 0
    m = 0
    for i in range(ind_t.n):
        if ver <= 2.11:
            p[i] = ind_t.frq.item(i)
        else:
            p[i] = ind_t.pos.item(i)

        if ind_t.type.item(i) == 1 and p[i] == 1:
            k[n] = i+1
            n = n+1
        if ind_t.type.item(i) == 1 and p[i] == 2:
            l[m] = i+1
            m = m+1

    if ver <= 2.11:
        if n >= 3:
            if val.item(k.item(0)) == 0 and val.item(k.item(1)) == 0:
                p[k[0]] = -1
                p[k[1]] = -1
            elif val.item(k.item(0)) != 0 and val.item(k.item(1)) == 0:
                p[k[0]] = 1
                p[k[1]] = -1
            elif val.item(k.item(0)) == 0 and val.item(k.item(1)) != 0:
                p[k[0]] = -1
                p[k[1]] = 1
            elif ind_t.pri.item(k.item(1)) > ind_t.pri.item(k.item(0)):
                p[k[0]] = -1
                p[k[1]] = 1
            else:
                p[k[0]] = 1
                p[k[1]] = -1

        if m >= 3:
            if val.item(l.item(0)) == 0 and val.item(l.item(1)) == 0:
                p[k[0]] = -1
                p[k[1]] = -1
            elif val.item(l.item(0)) != 0 and val.item(l.item(1)) == 0:
                p[k[0]] = 2
                p[k[1]] = -1
            elif val.item(l.item(0)) == 0 and val.item(l.item(1)) != 0:
                p[k[0]] = -1
                p[k[1]] = 2
            elif ind_t.pri.item(l.item(1)) > ind_t.pri.item(l.item(0)):
                p[k[0]] = -1
                p[k[1]] = 2
            else:
                p[k[0]] = 2
                p[k[1]] = -1

    for i in range(ind_t.n):
        if p.item(i) < 1 or val.item(i) == 0:
            continue
        if ind_t.type.item(i) == 1:
            data.P[int(p.item(i)-1), 0] = val.item(i)
            data.code[int(p.item(i)-1), 0] = ind_t.code.item(i)
        elif ind_t.type.item(i) == 2:
            data.L[int(p.item(i)-1), 0] = val.item(i)
            data.LLI[int(p.item(i)-1), 0] = lli.item(i)
        elif ind_t.type.item(i) == 3:
            data.D[int(p.item(i)-1), 0] = val.item(i)
        elif ind_t.type.item(i) == 4:
            data.S[int(p.item(i)-1), 0] = int(val.item(i)*4.0+0.5)

    return data, stat
