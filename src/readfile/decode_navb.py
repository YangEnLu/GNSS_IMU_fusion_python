from ..common.global_constants import nav, default_opt, headinfo, glc, gls
import numpy.matlib as npm
from .set_sysmask import set_sysmask
from ..common.satid2no import satid2no
from ..common.satsys import satsys
from ..common.satno import satno
from ..common.str2time import str2time
from .decode_geph import decode_geph
from .decode_eph import decode_eph
import numpy as np


def decode_navb(nav: nav, opt: str, headinfo: headinfo, fname: str, num_prev_line: int):
    NMAX = 10000
    stat = 1
    nav.eph = npm.repmat(gls().eph, NMAX, 1)
    nav.geph = npm.repmat(gls().geph, NMAX, 1)

    if headinfo.type == "N":
        sys = headinfo.sys
    elif headinfo.type == "G":
        sys = glc().SYS_GLO
    elif headinfo.type == "L":
        sys = glc().SYS_GAL
    elif headinfo.type == "J":
        sys = glc().SYS_QZS
    else:
        stat = 0

    fid = open(fname, "r")
    num_line = 0
    is_new_data = True
    for line in fid:
        num_line = num_line+1
        if num_line <= num_prev_line:
            continue
        else:
            if is_new_data:
                eph = gls().eph
                geph = gls().geph
                type = 0
                stat0 = 1
                data = np.zeros((1, 64))
                buff = " "*glc().MAXRNXLEN
                sp = 2
                i = 0
                mask = set_sysmask(opt)
                ver = headinfo.ver
                buff = line
                if ver >= 3.0 or sys == glc().SYS_GAL or sys == glc().SYS_QZS:
                    satid = buff[0:3]
                    sat = satid2no(satid)
                    sp = 3
                    if ver >= 3.0:
                        sys, prn = satsys(sat)
                    if sys == glc().SYS_NONE:
                        stat0 = 0
                else:
                    prn = float(buff[0:2])
                    if sys == glc().SYS_GLO:
                        sat = satno(glc().SYS_GLO, prn)
                    elif prn >= 93 and prn <= 97:
                        sat = satno(glc().SYS_QZS, prn+100)
                    else:
                        sat = satno(glc().SYS_GPS, prn)
                    if sys == glc().SYS_NONE:
                        stat0 = 0
                toc = str2time(buff[sp:sp+20])

                p = sp+20
                for j in range(3):
                    data[0, i] = float(buff[p:p+19])
                    i = i+1
                    p = p+19
                is_new_data = False
            else:
                buff = line
                p = sp+1
                for j in range(4):
                    if buff[p:p+19] == "                   ":
                        data[0, i] = 0
                        i = i+1
                        p = p+19
                        continue
                    data[0, i] = float(buff[p:p+19])
                    i = i+1
                    p = p+19

                if sys == glc().SYS_GLO and i >= 15:
                    if mask[sys] == 0:
                        stat0 = 0
                    type = 2
                    geph, stat0 = decode_geph(ver, sat, toc, data)
                    is_new_data = True
                elif i >= 31:
                    if mask[sys] == 0:
                        stat0 = 0
                    type = 1
                    eph, stat0 = decode_eph(ver, sat, toc, data)
                    is_new_data = True
                    
                    
                
                    
    return nav, stat
