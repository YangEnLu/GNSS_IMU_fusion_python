from ..common.global_constants import gls, glc, index, default_opt, headinfo, obsd, obs
from .set_sysmask import set_sysmask
from .set_index import set_index
from .decode_epoch import decode_epoch
from .decode_data import decode_data
from ..common.utc2gpst import utc2gpst
from ..readfile.saveslips import saveslips
from ..readfile.restslips import restslips
from ..common.screent import screent
import numpy as np
import numpy.matlib as npm
from tqdm import tqdm


def decode_obsb(headinfo: headinfo, obs: obs, tobs, opt: default_opt, fname: str, num_prev_line: int):
    slips = np.zeros((glc().MAXSAT, glc().NFREQ))
    obs.data = npm.repmat(obsd(), 100000, 1)

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
    for line in tqdm(fid):
        num_line = num_line+1
        if num_line <= num_prev_line:
            continue
        else:
            # read record of every epoch
            if is_header == 1:
                data = npm.repmat(gls().obsd, glc().MAXOBS, 1)
                time, nsat, sats, flag = decode_epoch(headinfo.ver, line)
                is_header = 0
                ndata = 0
            else:
                if i < nsat:
                    if nsat <= 0:
                        continue
                    elif flag == 3 or flag == 4:
                        continue
                    elif flag <= 2 or flag == 6:
                        data0 = obsd()
                        data0.time = time
                        data0.sat = sats[i]
                        data0, stat = decode_data(
                            line, headinfo.ver, data0, mask, ind)
                        if stat == 1:
                            data[ndata, 0] = data0
                            ndata = ndata+1
                    i = i+1
                if i == nsat:
                    i = 0
                    is_header = 1
                    # save data to obs class
                    if ndata == 0:
                        continue
                    for id in range(ndata):
                        if headinfo.tsys == glc().TSYS_UTC:
                            data[id, 0].time = utc2gpst(data[id, 0].time)
                        data[id, 0], slips = saveslips(data[id, 0], slips)
                    if not screent(data[id, 0].time, opt.ts, opt.te, opt.ti):
                        continue
                    for id in range(ndata):
                        if obs.n+1 > np.shape(obs.data)[0]:
                            obs.data = np.append(
                                obs.data, npm.repmat(obsd(), 100000, 1), axis=0)
                        data[id, 0], slips = restslips(data[id, 0], slips)
                        obs.data[obs.n, 0] = data[id, 0]
                        obs.n = obs.n+1
                        
                    del data

    if obs.n < np.shape(obs.data)[0]:
        obs.data = obs.data[0:obs.n, ]

    return obs
