from ..common.global_constants import glc, gls, default_opt, default_file
from ..common.initoutfile import initoutfile
from ..readfile.read_infile import read_infile
from ..readfile.adjobs import adjobs
from ..readfile.adjnav import adjnav
from .gnss_processor import gnss_processor
import time


def exepos(opt: default_opt, file: default_file):
    st = time.time()
    rtk = gls().rtk

    # read input file
    obsr, obsb, nav, imu = read_infile(opt, file)

    # initialize output file
    rtk = initoutfile(rtk, opt, file, obsr)

    # high efficiency by converting struct to matrix
    obsr = adjobs(obsr, opt)
    obsb = adjobs(obsb, opt)
    nav = adjnav(nav, opt)
    
    
    # process all data
    if opt.ins.mode == glc().GIMODE_OFF:
        # GNSS
        gnss_processor(rtk,opt,obsr,obsb,nav)
    elif opt.ins.mode == glc().GIMODE_LC or opt.ins.mode == glc().GIMODE_TC:
        pass
        
    
    
    
    
    et = time.time()
    elapsed_time = et - st
    print(f'Total processing time : {elapsed_time:.2f}')
    
