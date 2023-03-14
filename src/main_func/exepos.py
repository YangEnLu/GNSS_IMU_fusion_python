from ..common.global_constants import glc, gls
from ..readfile.read_infile import read_infile
import time


def exepos(opt, file):
    st = time.time()
    rtk = gls().rtk

    # read input file
    obsr, obsb, nav, imu = read_infile(opt, file)

    et = time.time()
    elapsed_time = et - st
    
    
    return rtk
