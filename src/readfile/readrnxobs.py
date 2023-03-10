from ..common.global_constants import glc, default_opt
from .decode_rnxh import decode_rnxh
from .decode_obsh import decode_obsh
from .decode_obsb import decode_obsb


def readrnxobs(obs, nav, opt: default_opt, fname: str):
    fname0 = fname.split(glc().sep)[-1]
    print(f"Info:reading obs file {fname0}")

    # read rinex header
    headinfo = decode_rnxh(fname)
    if headinfo.type != "O":
        print(f"The file {fname} is not rinex observation file!!!")

    # decode file header
    headinfo, nav, obs, tobs, num_prev_line = decode_obsh(
        headinfo, nav, obs, fname)

    # decode body
    obs = decode_obsb(headinfo, obs, tobs, opt, fname, num_prev_line)

    return obs, nav
