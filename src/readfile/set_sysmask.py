import numpy as np


def set_sysmask(opt: str):
    mask = np.zeros(5)
    if opt.find("G") != -1:
        mask[0] = 1
    if opt.find("R") != -1:
        mask[1] = 1
    if opt.find("E") != -1:
        mask[2] = 1
    if opt.find("C") != -1:
        mask[3] = 1
    if opt.find("J") != -1:
        mask[4] = 1

    return mask
