from ..common.global_constants import gls, glc, default_file, default_opt
from .readrnxobs import readrnxobs
from .readrnxnav import readrnxnav


def read_infile(opt: default_opt, file: default_file):
    obsr = gls().obs
    obsb = gls().obs
    nav = gls().nav
    imu = gls().imu

    # read rover observation file
    if not file.obsr == "":
        obsr, nav = readrnxobs(obsr, nav, opt, file.obsr)
        if obsr.n == 0:
            print("<read_infile>ERROR: Number of rover obs is zero!!!")
    else:
        print("<read_infile>ERROR: Have no observation file for rover!!!")

    # read base observation file
    if not file.obsb == "":
        obsb, nav = readrnxobs(obsb, nav, opt, file.obsb)
        if obsb.n == 0 and opt.mode >= glc().PMODE_DGNSS and opt.mode <= glc().PMODE_STATIC:
            print("<read_infile>ERROR: Number of base obs is zero!!!")
    else:
        if opt.mode >= glc().PMODE_DGNSS and opt.mode <= glc().PMODE_STATIC:
            print(
                "<read_infile>ERROR: Relative positioning mode,but have no observation file for base station!!!")

    if not file.beph == "":
        nav = readrnxnav(nav, opt, file.beph)
        pass

    return obsr, obsb, nav, imu
