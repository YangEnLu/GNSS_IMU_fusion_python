from .global_constants import rtk, default_opt, default_file, obs, glc


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
    
