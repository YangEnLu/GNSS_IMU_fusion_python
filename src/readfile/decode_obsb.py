from ..common.global_constants import gls, glc, index
from .set_sysmask import set_sysmask
from .set_index import set_index
from .decode_epoch import decode_epoch
from .decode_data import decode_data
import numpy as np
import numpy.matlib as npm


def decode_obsb(headinfo, obs, tobs, opt, fname, num_prev_line):
    slips = np.zeros((glc().MAXSAT, glc().NFREQ))
    obs.data = npm.repmat(gls().obsd, 100000, 1)

    # set system mask
    mask = set_sysmask(opt.navsys)

    # set signal index
    ind = npm.repmat(index(), 1, 5)
    ind[0, 0] = set_index(headinfo.ver, glc().SYS_GPS, opt, tobs[:, 0])
    ind[0, 1] = set_index(headinfo.ver, glc().SYS_GLO, opt, tobs[:, 1])
    ind[0, 2] = set_index(headinfo.ver, glc().SYS_GAL, opt, tobs[:, 2])
    ind[0, 3] = set_index(headinfo.ver, glc().SYS_BDS, opt, tobs[:, 3])
    ind[0, 4] = set_index(headinfo.ver, glc().SYS_QZS, opt, tobs[:, 4])

    # read body
    fid = open(fname, "r")
    num_line = 0
    is_header = 1
    i = 0
    ndata = 0
    for line in fid:
        num_line = num_line+1
        if num_line <= num_prev_line:
            continue
        else:
            # read record of every epoch
            data = npm.repmat(gls().obsd, glc().MAXOBS, 1)
            if is_header == 1:
                time, nsat, sats, flag = decode_epoch(headinfo.ver, line)
                is_header = 0
            else:
                if i <= nsat:
                    if nsat <= 0:
                        continue
                    elif flag == 3 or flag == 4:
                        continue
                    elif flag <= 2 or flag == 6:
                        data0 = gls().obsd
                        data0.time = time
                        data0.sat = sats[i]
                        data0, stat = decode_data(line, headinfo.ver, data0, mask, ind)
                    i = i+1
                if i > nsat:
                    i = 0
                    is_header = 1
    return obs
