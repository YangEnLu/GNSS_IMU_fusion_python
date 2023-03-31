from ...common.global_constants import glc, default_opt
import numpy as np


def varerr_spp(opt: default_opt, el, sys):
    if sys == glc().SYS_GLO:
        fact = glc().EFACT_GLO
    else:
        fact = glc().EFACT_GPS

    varr = (opt.err[0]**2)*(opt.err[1]**2+opt.err[2]**2/np.sin(el))
    if opt.ionoopt == glc().IONOOPT_IFLC:
        varr = 3**2*varr
    var = fact**2*varr
    
    return var
