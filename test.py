import sys
import os
import numpy as np
from time import perf_counter

# if __name__ == '__main__':
from src.common.global_constants import glc, gls
from src.gui.GNSSIMUCfg import OpenUI
from src.readfile.decode_cfg import decode_cfg
from src.readfile.decode_rnxh import decode_rnxh
from src.readfile.decode_obsh import decode_obsh
from src.readfile.readrnxobs import readrnxobs
from src.readfile.readrnxnav import readrnxnav
from src.main_func.exepos import exepos


# Open input UI
opt, file, gui_flag = OpenUI()

rtk = gls().rtk
# read input file
obsr = gls().obs
obsb = gls().obs
nav = gls().nav
imu = gls().imu
# obsr, nav = readrnxobs(obsr, nav, opt, file.obsr)
# nav = readrnxnav(nav, opt, file.beph)
exepos(opt,file)
