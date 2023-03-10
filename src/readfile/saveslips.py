from ..common.global_constants import glc, obsd


def saveslips(data: obsd, slips):
    for i in range(glc().NFREQ):
        if int(data.LLI[i, 0]) & 1:
            slips[data.sat-1, i] = int(slips[data.sat-1, i]) | 1

    return data, slips
