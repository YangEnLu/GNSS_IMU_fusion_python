from ..common.global_constants import glc, index
from .find_str import find_str
import numpy as np
from ..common.obs2code import obs2code
from ..common.getcodepri import getcodepri


def set_index(ver, sys, opt, tobs):
    obscodes = "CLDS"
    ind = index()
    nn = np.size(tobs, 0)
    n = 0
    for i in range(nn):
        if tobs[i] == "":
            break
        if obscodes.find(tobs[i][0]) == -1:
            break

        ind.code[0, i], ind.frq[0, i] = obs2code(tobs[i][1:3], sys)

        typ = find_str(obscodes, tobs[i][0])
        if len(typ) != 0:
            ind.type[0, i] = typ[0]+1
        else:
            ind.type[0, i] = 0

        ind.pri[0, i] = getcodepri(sys, ind.code[0, i], opt)
        ind.pos[0, i] = -1
        ind.code[0, i] = ind.code[0, i]-1
        n = n+1

    for i in range(glc().MAXFREQ):
        # search for the highest level code
        k = -1
        for j in range(n):
            if ind.frq[0,j] == i+1 and ind.pri[0,j] != 0 and (k < 0 or ind.pri[0,j] > ind.pri[0,k]):
                k = j
        if k<0:
            continue
        for j in range(n):
            if ind.code[0,j]==ind.code[0,k]:
                ind.pos[0,j]=i+1
    
    ind.n=n
    return ind
