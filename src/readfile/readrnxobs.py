from ..common.global_constants import glc
from .decode_rnxh import decode_rnxh
from .decode_obsh import decode_obsh


def readrnxobs(obs, nav, opt, fname: str):
    fname0 = fname.split(glc().sep)[-1]
    print(f"Info:reading obs file {fname0}")
    
    # read rinex header
    headinfo = decode_rnxh(fname)
    if headinfo.type != "O":
        print(f"The file {fname} is not rinex observation file!!!")

    # decode file header
    decode_obsh_error = decode_obsh(headinfo, nav, obs, fname)


    # decode body

    return headinfo
