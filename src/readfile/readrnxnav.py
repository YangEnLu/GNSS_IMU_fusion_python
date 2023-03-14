from ..common.global_constants import glc, default_opt, nav
from .decode_rnxh import decode_rnxh
from .decode_navh import decode_navh


def readrnxnav(nav: nav, opt: default_opt, fname: str):
    fname0 = fname.split(glc().sep)[-1]
    print(f"Info:reading nav file {fname0}")

    # read rinex header
    # headinfo = decode_rnxh(fname0)
    nav, prev_num_line = decode_navh(nav,fname0)
    
