from ..common.global_constants import glc, rtk, default_opt
from .str2time import str2time
from ..readfile.set_sysmask import set_sysmask
import numpy as np


def initrtk(rtk: rtk, opt: default_opt):

    rtk.opt = opt
    rtk.opt.ts = str2time(rtk.opt.ts)
    rtk.opt.te = str2time(rtk.opt.te)
    rtk.mask = set_sysmask(opt.navsys)

    if opt.mode <= glc().PMODE_STATIC:
        if opt.ionoopt == glc().IONOOPT_IFLC:
            NF = 1
        else:
            NF = opt.nf
        if opt.dynamics == 1:
            NP = 9
        else:
            NP = 3
        if opt.ionoopt == glc().IONOOPT_EST:
            NI = glc().MAXSAT
        else:
            NI = 0
        if opt.tropopt < glc().TROPOPT_EST:
            NT = 0
        elif opt.tropopt == glc().TROPOPT_EST:
            NT = 2
        else:
            NT = 6
        if opt.glomodear != 2:
            NL = 0
        else:
            NL = 2
        if opt.mode <= glc().PMODE_DGNSS:
            NB = 0
        else:
            NB = NF*glc().MAXSAT

        # number of parameter
        NR = NP+NI+NT+NL
        NX = NR+NB
        rtk.NF = NF
        rtk.NP = NP
        rtk.NI = NI
        rtk.NT = NT
        rtk.NL = NL
        rtk.NB = NB

        # index of parameter
        II = NP
        ITR = NP+NI
        ITB = NP+NI+NT/2
        IL = NP+NI+NT
        IB = NR
        rtk.ii = II
        rtk.itr = ITR
        rtk.itb = ITB
        rtk.il = IL
        rtk.ib = IB
    else:
        if opt.ionoopt == glc().IONOOPT_IFLC:
            NF = 1
        else:
            NF = opt.nf
        if opt.dynamics == 1:
            NP = 9
        else:
            NP = 3
        NC = glc().NSYS

        # for glonass inter-frequency code bias
        if opt.gloicb == 0:
            NICB = 0
        elif opt.gloicb == glc().GLOICB_LNF:
            NICB = 1
        else:
            NICB = 2

        if opt.tropopt < glc().TROPOPT_EST:
            NT = 0
        elif opt.tropopt == glc().TROPOPT_EST:
            NT = 1
        else:
            NT = 3

        if opt.ionoopt == glc().IONOOPT_EST:
            NI = glc().MAXSAT
        else:
            NI = 0

        if opt.nf >= 3:
            ND = 1
        else:
            ND = 0

        # number of parameters
        NR = NP+NC+NICB+NT+NI+ND
        NB = NF*glc().MAXSAT
        NX = NR+NB
        rtk.NF = NF
        rtk.NP = NP
        rtk.NC = NC
        rtk.NICB = NICB
        rtk.NT = NT
        rtk.NI = NI
        rtk.ND = ND
        rtk.NB = NB

        # index of parameter
        IC = NP
        IICB = NP+NC
        IT = NP+NC+NICB
        II = NP+NC+NICB+NT
        ID = NP+NC+NICB+NT+NI
        IB = NR
        rtk.ic = IC
        rtk.iicb = IICB
        rtk.it = IT
        rtk.ii = II
        rtk.id = ID
        rtk.ib = IB

    rtk.nx = NX
    rtk.na = NR
    rtk.x = np.zeros((rtk.nx, 1))
    rtk.P = np.zeros((rtk.nx, rtk.nx))
    rtk.xa = np.zeros((rtk.na, 1))
    rtk.Pa = np.zeros((rtk.na, rtk.na))

    return rtk
