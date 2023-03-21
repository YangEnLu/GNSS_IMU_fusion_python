from .global_constants import glc, nav
from .satsys import satsys


def satwavelen(sat: float, frq: float, nav: nav):
    lam = 0
    sys, prn = satsys(sat)

    if sys == glc().SYS_GPS:
        if frq == 1:
            lam = glc().CLIGHT/glc().FREQ_GPS_L1  # L1
        elif frq == 2:
            lam = glc().CLIGHT/glc().FREQ_GPS_L2  # L2
        elif frq == 3:
            lam = glc().CLIGHT/glc().FREQ_GPS_L5  # L5
    elif sys == glc().SYS_GLO:
        if frq == 1:  # G1
            if nav.ng == 0:
                return lam
            for i in range(nav.ng):
                if nav.geph[i, 0].sat != sat:
                    continue
                lam = glc().CLIGHT/(glc().FREQ_GLO_G1 +
                                    glc().FREQ_GLO_D1*nav.geph[i, 0].frq)
        elif frq == 2: # G2
            if nav.ng==0:
                return lam
            for i in range(nav.ng):
                if nav.geph[i, 0].sat != sat:
                    continue
                lam = glc().CLIGHT/(glc().FREQ_GLO_G2 +
                                    glc().FREQ_GLO_D2*nav.geph[i, 0].frq)
        elif frq == 3: #G3
            lam = glc().CLIGHT/glc().FREQ_GLO_G3
    elif sys == glc().SYS_GAL:
        if frq == 1:
            lam = glc().CLIGHT/glc().FREQ_GAL_E1 # E1
        elif frq == 2:
            lam = glc().CLIGHT/glc().FREQ_GAL_E5A # E5a
        elif frq == 3:
            lam = glc().CLIGHT/glc().FREQ_GAL_E5B # E5b
        elif frq == 4:
            lam = glc().CLIGHT/glc().FREQ_GAL_E5AB # E5ab    
        elif frq == 5:
            lam = glc().CLIGHT/glc().FREQ_GAL_E6 # E6   
    elif sys == glc().SYS_BDS:
        if frq == 1:
            lam = glc().CLIGHT/glc().FREQ_BDS_B1 # B1
        elif frq == 2:
            lam = glc().CLIGHT/glc().FREQ_BDS_B2 # B2
        elif frq == 3:
            lam = glc().CLIGHT/glc().FREQ_BDS_B3 # B3
        elif frq == 4:
            lam = glc().CLIGHT/glc().FREQ_BDS_B1C # B1C
        elif frq == 5:
            lam = glc().CLIGHT/glc().FREQ_BDS_B2A # B2a
        elif frq == 6:
            lam = glc().CLIGHT/glc().FREQ_BDS_B2B # B2b   
    elif sys == glc().SYS_QZS:
        if frq == 1:
            lam = glc().CLIGHT/glc().FREQ_QZS_L1 # L1
        elif frq == 2:
            lam = glc().CLIGHT/glc().FREQ_QZS_L2 # L2
        elif frq == 3:
            lam = glc().CLIGHT/glc().FREQ_QZS_L5 # L5
        elif frq == 4:
            lam = glc().CLIGHT/glc().FREQ_QZS_L6 # L6/LEX
        
    return lam
