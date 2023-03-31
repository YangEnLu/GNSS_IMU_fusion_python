from .global_constants import glc, nav, obsd, default_opt
from .satsys import satsys
import numpy as np


def getdcb(nav: nav, obs: obsd, opt: default_opt):
    use_dcb_flag = 1
    dcb = np.zeros((glc().NFREQ, 1))
    cbias = nav.cbias
    sat = int(obs.sat)
    sys, prn = satsys(sat)
    if sys == glc().SYS_NONE:
        return dcb, use_dcb_flag

    if sys == glc().SYS_GPS:
        DCB_p1p2 = cbias[sat-1, glc().GPS_C1WC2W-1]
        a = glc().FREQ_GPS_L1**2 - glc().FREQ_GPS_L2**2
        alpha = glc().FREQ_GPS_L1**2/a
        beta = -glc().FREQ_GPS_L2**2/a
        if DCB_p1p2 == 0:
            use_dcb_flag = 0
        for i in range(glc().NFREQ):
            if obs.code[i, 0] == glc().CODE_NONE:
                dcb[i, 0] = 0
                continue
            if i == 1:  # L1
                dcb[i, 0] = beta*DCB_p1p2
                if obs.code[i, 0] == glc().CODE_L1C:
                    dcb[i, 0] = dcb[i, 0] + cbias[sat-1, glc().GPS_C1CC1W-1]
            elif i == 2:  # L2
                dcb[i, 0] = -alpha*DCB_p1p2
                if obs.code[i, 0] == glc().CODE_L2C:
                    dcb[i, 0] = dcb[i, 0]+cbias[sat-1, glc().GPS_C2CC2W-1]
                elif obs.code[i, 0] == glc().CODE_L2S:
                    dcb[i, 0] = dcb[i, 0]-cbias[sat-1, glc().GPS_C2WC2S-1]
                elif obs.code[i, 0] == glc().CODE_L2L:
                    dcb[i, 0] = dcb[i, 0]-cbias[sat-1, glc().GPS_C2WC2L-1]
                elif obs.code[i, 0] == glc().CODE_L2X:
                    dcb[i, 0] = dcb[i, 0]-cbias[sat-1, glc().GPS_C2WC2X-1]
            elif i == 3:  # L3
                DCB_p1p3 = 0
                beta_13 = -glc().FREQ_GPS_L5**2/(glc().FREQ_GPS_L1**2-glc().FREQ_GPS_L5**2)
                if obs.code[i, 0] == glc().CODE_L5Q:
                    DCB_p1p3 = cbias[sat-1, glc().GPS_C1CC5Q-1] - \
                        cbias[sat-1, glc().GPS_C1CC1W-1]
                elif obs.code[i, 0] == glc().CODE_L5X:
                    DCB_p1p3 = cbias[sat-1, glc().GPS_C1CC5X-1] - \
                        cbias[sat-1, glc().GPS_C1CC1W-1]
                dcb[i, 0] = beta_13*DCB_p1p2-DCB_p1p3
    elif sys == glc().SYS_GLO:
        DCB_p1p2 = cbias[sat-1, glc().GLO_C1PC2P-1]
        a = glc().FREQ_GLO_G1 ** 2-glc().FREQ_GLO_G2 ** 2
        alpha = glc().FREQ_GLO_G1**2/a
        beta = -glc().FREQ_GLO_G2**2/a
        if DCB_p1p2 == 0:
            use_dcb_flag = 0
        for i in range(glc().NFREQ):
            if obs.code[i, 0] == glc().CODE_NONE:
                dcb[i, 0] = 0
                continue
            if i == 1:  # G1
                dcb[i, 0] = beta*DCB_p1p2
                if obs.code[i, 0] == glc().CODE_L1C:
                    dcb[i, 0] = dcb[i, 0]+cbias[sat-1, glc().GLO_C1CC1P-1]
            elif i == 2:  # G2
                dcb[i, 0] = -alpha*DCB_p1p2
                if obs.code[i, 0] == glc().CODE_L2C:
                    dcb[i, 0] = dcb[i, 0]+cbias[sat-1, glc().GLO_C2CC2P-1]
    elif sys == glc().SYS_GAL:
        DCB_p1p2 = cbias[sat-1, glc().GAL_C1CC5Q-1]
        a = glc().FREQ_GAL_E1**2-glc().FREQ_GAL_E5A**2
        alpha = glc().FREQ_GAL_E1 ** 2/a
        beta = -glc().FREQ_GAL_E5A ** 2/a
        if DCB_p1p2 == 0:
            use_dcb_flag = 0
        for i in range(glc().NFREQ):
            if obs.code[i, 0] == glc().CODE_NONE:
                dcb[i, 0] = 0
                continue
            if i == 1:  # E1
                if obs.code[i, 0] == glc().CODE_L1X:
                    DCB_p1p2 = cbias[sat-1, glc.GAL_C1XC5X-1]
                dcb[i, 0] = beta*DCB_p1p2
            elif i == 2:  # E5A
                if obs.code[i, 0] == glc().CODE_L5X:
                    DCB_p1p2 = cbias[sat-1, glc.GAL_C1XC5X-1]
                dcb[i, 0] = -alpha*DCB_p1p2
            elif i == 2:  # E5B
                DCB_p1p3 = 0
                beta_13 = -glc().FREQ_GAL_E5B**2/(glc().FREQ_GAL_E1**2-glc().FREQ_GAL_E5B**2)
                if obs.code[i, 0] == glc().CODE_L7X:
                    DCB_p1p2 = cbias[sat-1, glc().GAL_C1XC5X-1]
                    DCB_p1p3 = cbias[sat-1, glc().GAL_C1XC7X-1]
                elif obs.code[i, 0] == glc().CODE_L7Q:
                    DCB_p1p3 = cbias[sat-1, glc().GAL_C1CC7Q-1]
                dcb[i, 0] = beta_13*DCB_p1p2-DCB_p1p3
    elif sys == glc().SYS_BDS:
        if opt.sateph == glc().EPHOPT_BRDC:  # based on b3
            if prn > 18:  # BD3
                DCB_b1b3 = cbias[sat-1, glc().BD3_C2IC6I-1]
                if DCB_b1b3 == 0:
                    use_dcb_flag = 0
                for i in range(glc().NFREQ):
                    if obs.code[i, 0] == glc().CODE_NONE:
                        dcb[i, 0] = 0
                        continue
                    elif obs.code[i, 0] == glc().CODE_L2I:  # B1
                        dcb[i, 0] = DCB_b1b3
                    elif obs.code[i, 0] == glc().CODE_L7I:  # B2
                        dcb[i, 0] = 0
                    elif obs.code[i, 0] == glc().CODE_L6I:  # B3
                        dcb[i, 0] = 0
                    elif obs.code[i, 0] == glc().CODE_L1X:  # B1C
                        dcb[i, 0] = cbias[sat-1, glc().BD3_C1XC6I-1]
                    elif obs.code[i, 0] == glc().CODE_L1P:  # B2a
                        dcb[i, 0] = cbias[sat-1, glc().BD3_C1XC6I-1] - \
                            cbias[sat-1, glc().BD3_C1XC5X-1]
                    elif obs.code[i, 0] == glc().CODE_L5P:  # B2a
                        dcb[i, 0] = cbias[sat-1, glc().BD3_C1PC6I-1] - \
                            cbias[sat-1, glc.BD3_C1PC5P-1]
                    elif obs.code[i, 0] == glc().CODE_L5D:  # B2a
                        dcb[i, 0] = cbias[sat-1, glc().BD3_C1DC6I-1] - \
                            cbias[sat-1, glc().BD3_C1DC5D-1]
            else:  # BD2
                bd2frq = opt.bd2frq
                DCB_b1b2 = cbias[sat-1, glc().BD2_C2IC7I-1]
                DCB_b1b3 = cbias[sat-1, glc().BD2_C2IC6I-1]
                if DCB_b1b2 == 0 or DCB_b1b3 == 0:
                    use_dcb_flag = 0
                for i in range(glc().NFREQ):
                    if obs.code[i, 0] == glc().CODE_NONE:
                        dcb[i, 0] = 0
                        continue
                    if bd2frq[i] == 1:
                        dcb[i, 0] = DCB_b1b3
                    elif bd2frq[i] == 2:
                        dcb[i, 0] = DCB_b1b3-DCB_b1b2
                    elif bd2frq[i] == 3:
                        dcb[i, 0] = 0
        elif opt.sateph == glc().EPHOPT_PREC:
            # TODO Precise
            pass
        elif opt.gnsproac == glc().AC_WUM or opt.gnsproac == glc().AC_GBM:  # based on B1B3
            # TODO gnsproac
            bd2frq = opt.bd2frq
            bd3frq = opt.bd3frq
            a = glc().FREQ_BDS_B1**2-glc().FREQ_BDS_B3**2
            alpha = glc().FREQ_BDS_B1**2/a
            beta = -glc().FREQ_BDS_B3**2/a

        else:  # BD2
            DCB_b1b2 = cbias[sat-1, glc().BD2_C2IC7I-1]
            DCB_b1b3 = cbias[sat-1, glc().BD2_C2IC6I-1]
            if bd2frq[i] == 1:
                dcb[i, 0] = beta*DCB_b1b3
            elif bd2frq[i] == 2:
                beta_13 = -glc().FREQ_BDS_B2/(glc().FREQ_BDS_B1**2-glc().FREQ_BDS_B2**2)
                dcb[i, 0] = beta_13*DCB_b1b3-DCB_b1b2
            elif bd2frq[i] == 3:
                dcb[i, 0] = -alpha*DCB_b1b3
    elif sys == glc().SYS_QZS:  # QZSS
        # TODO QZSS
        pass

    return dcb, use_dcb_flag
