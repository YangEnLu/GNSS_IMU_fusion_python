import sys
import os
import numpy as np


# def fast_scandir(dirname):
#     subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
#     for dirname in list(subfolders):
#         subfolders.extend(fast_scandir(dirname))
#     return subfolders

# # Add path
# cwd = os.getcwd()
# subfolders = fast_scandir(cwd)
# sys.path.append(subfolders)


if __name__ == '__main__':
    # Add src
    from src.common.global_constants import glc, gls
    from src.gui.GNSSIMUCfg import OpenUI
    from src.readfile.decode_cfg import decode_cfg
    from src.main_func.exepos import exepos

    # Open input UI
    opt, file, gui_flag = OpenUI()

    if gui_flag:
        print("Run")
        exepos(opt,file)
        input("Press any button to exit")
    else:
        print("Quit")
        input("Press any button to exit")
        sys.exit()
    
    