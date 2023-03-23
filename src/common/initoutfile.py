from .global_constants import rtk, default_opt, default_file, obs, glc
# from ..main_func.exepos import exepos
from .outsolhead import outsolhead
import inspect
import os


def initoutfile(rtk: rtk, opt: default_opt, file: default_file, obsr: obs):
    if opt.ins.mode == glc().GIMODE_OFF:
        if opt.mode == glc().PMODE_SPP:
            mode = "SPP"
        elif opt.mode == glc().PMODE_DGNSS:
            mode = "PPD"
        elif opt.mode == glc().PMODE_KINEMA:
            mode = "PPK"
        elif opt.mode == glc().PMODE_STATIC:
            mode = "PPS"
        elif opt.mode == glc().PMODE_PPP_KINEMA:
            mode = "PPP_K"
        elif opt.mode == glc().PMODE_PPP_STATIC:
            mode = "PPP_S"
    elif opt.ins.mode == glc().GIMODE_LC:
        if opt.mode == glc().PMODE_SPP:
            mode = "SPP_LC"
        elif opt.mode == glc().PMODE_DGNSS:
            mode = "PPD_LC"
        elif opt.mode == glc().PMODE_KINEMA:
            mode = "PPK_LC"
        elif opt.mode == glc().PMODE_PPP_KINEMA:
            mode = "PPP_LC"
    elif opt.ins.mode == glc().GIMODE_TC:
        if opt.mode == glc().PMODE_SPP:
            mode = "SPP_TC"
        elif opt.mode == glc().PMODE_DGNSS:
            mode = "PPD_TC"
        elif opt.mode == glc().PMODE_KINEMA:
            mode = "PPK_TC"
        elif opt.mode == glc().PMODE_PPP_KINEMA:
            mode = "PPP_TC"

    fullname = file.obsr
    outfilename = fullname.split("/")[-1].split(".")[0]+"_"+mode+".pos"
    fullpath = os.path.realpath(__file__)
    fullpath = glc().sep.join(fullpath.split(glc().sep)[0:2])
    pathname = fullpath+glc().sep+"result"+glc().sep
    rtk.outfile = pathname+outfilename

    outsolhead(rtk, opt, obsr)

    return rtk
