from ..common.global_constants import obs, default_opt, glc
from ..common.satsys import satsys
import numpy as np


def adjobs(obs: obs, opt: default_opt):
    data0 = np.zeros((obs.n, 3+6*glc().NFREQ))

    if obs.n == 0:
        return obs

    bds_frq_flag = 1
    data = obs.data
    del obs.data

    if glc().NFREQ > 3 and (len(opt.bd2frq) <= 3 or len(opt.bd3frq) <= 3 and opt.navsys.find("C") != -1):
        bds_frq_flag = 0
        print("Warning:Specified frequency of BDS less than used number of frequency!")

    for i in range(obs.n):
        P = np.zeros((1, glc().NFREQ))
        L = np.zeros((1, glc().NFREQ))
        D = np.zeros((1, glc().NFREQ))
        S = np.zeros((1, glc().NFREQ))
        LLI = np.zeros((1, glc().NFREQ))
        code = np.zeros((1, glc().NFREQ))
        sys, prn = satsys(data[i, 0].sat)

        if sys == glc().SYS_BDS:  # BDS
            if prn < 19:  # BD2
                if not bds_frq_flag:
                    continue
                frq = opt.bd2frq
                for j in range(glc().NFREQ):
                    P[0, j] = data[i, 0].P[int(frq[j]), 0]
                    L[0, j] = data[i, 0].L[int(frq[j]), 0]
                    D[0, j] = data[i, 0].D[int(frq[j]), 0]
                    S[0, j] = data[i, 0].S[int(frq[j]), 0]
                    LLI[0, j] = data[i, 0].LLI[int(frq[j]), 0]
                    code[0, j] = data[i, 0].code[int(frq[j]), 0]
            else:  # BD3
                if not bds_frq_flag:
                    continue
                frq = opt.bd3frq
                for j in range(glc().NFREQ):
                    P[0, j] = data[i, 0].P[int(frq[j]), 0]
                    L[0, j] = data[i, 0].L[int(frq[j]), 0]
                    D[0, j] = data[i, 0].D[int(frq[j]), 0]
                    S[0, j] = data[i, 0].S[int(frq[j]), 0]
                    LLI[0, j] = data[i, 0].LLI[int(frq[j]), 0]
                    code[0, j] = data[i, 0].code[int(frq[j]), 0]
        else:  # GPS GLO GAL QZS
            for j in range(glc().NFREQ):
                P[0, j] = data[i, 0].P[j, 0]
                L[0, j] = data[i, 0].L[j, 0]
                D[0, j] = data[i, 0].D[j, 0]
                S[0, j] = data[i, 0].S[j, 0]
                LLI[0, j] = data[i, 0].LLI[j, 0]
                code[0, j] = data[i, 0].code[j, 0]

        time = data[i, 0].time
        sat = data[i, 0].sat
        data0[i, 0:3] = [time.time, time.sec, sat]
        data0[i, 3:3+glc().NFREQ] = P.tolist()[0]
        data0[i, 3+glc().NFREQ:3+2*glc().NFREQ] = L.tolist()[0]
        data0[i, 3+2*glc().NFREQ:3+3*glc().NFREQ] = D.tolist()[0]
        data0[i, 3+3*glc().NFREQ:3+4*glc().NFREQ] = S.tolist()[0]
        data0[i, 3+4*glc().NFREQ:3+5*glc().NFREQ] = LLI.tolist()[0]
        data0[i, 3+5*glc().NFREQ:3+6*glc().NFREQ] = code.tolist()[0]

    obs.data = data0
    return obs
