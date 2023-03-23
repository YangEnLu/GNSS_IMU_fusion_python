from ..common.global_constants import glc, gls
from ..common.initoutfile import initoutfile
from ..readfile.read_infile import read_infile
import time


def exepos(opt, file):
    rtk = gls().rtk

    # read input file
    obsr, obsb, nav, imu = read_infile(opt, file)

    # initialize output file
    rtk = initoutfile(rtk,opt,file,obsr)
    
    return rtk
