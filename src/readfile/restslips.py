from ..common.global_constants import glc, obsd
import numpy as np


def restslips(data: obsd, slips: np.ndarray):
    for i in range(glc().NFREQ):
        if int(slips[data.sat-1, i]) & 1:
            data.LLI[i, 0] = int(data.LLI[i, 0]) | 1
        
        slips[int(data.sat-1), i] = 0

    return data, slips
