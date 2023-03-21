from ..common.global_constants import glc, default_opt, nav
from .decode_rnxh import decode_rnxh
from .decode_navh import decode_navh
from .decode_navb import decode_navb
from ..common.uniqnav import uniqnav
import time


def readrnxnav(nav: nav, opt: default_opt, fname: str):
    fname0 = fname.split(glc().sep)[-1]
    print(f"Info:reading nav file {fname0}")

    st = time.time()
    # read rinex header
    headinfo = decode_rnxh(fname0)
    nav, prev_num_line = decode_navh(nav, fname0)

    # read nav body
    nav, stat = decode_navb(nav, opt.navsys, headinfo, fname0, prev_num_line)
    et = time.time()
    elapsed_time = et - st
    if stat == 0:
        print(
            f"Unsupported rinex nav message {headinfo.ver:.2f} {headinfo.type}!!!")
    print(f'Decoding navigation file time: {elapsed_time:.2f} seconds')

    # sort and unique nav
    nav = uniqnav(nav)

    print("over")
    return nav
