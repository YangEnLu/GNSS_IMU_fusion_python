from ..common.global_constants import glc, gls, headinfo
from .find_str import find_str
from .convcode import convcode
import numpy as np


def decode_obsh(headinfo, nav, obs, fname):
    fid = open(fname, "r")
    tobs = np.empty((glc().MAXOBSTYPE, 3, glc().NSYS), dtype='str')
    delt = np.zeros((3, 1))
    sta = gls().sta
    decode_err = True
    for line in fid:
        label = line[60:-1]
        if len(line) <= 60:
            continue
        elif label.find("MARKER NAME") != -1:
            string = line[0:60]
            sta.name = string.split()[0]
        elif label.find("MARKER NUMBER") != -1:
            string = line[0:20]
            sta.maker = string.split()[0]
        elif label.find("MARKER TYPE") != -1:
            continue
        elif label.find("OBSERVER / AGENCY") != -1:
            continue
        elif label.find("REC # / TYPE / VERS") != -1:
            string = line[0:20]
            sta.recsno = string.split()[0]
            string = line[20:40]
            sta.rectype = string.split()[0]
            string = line[40:60]
            sta.recver = string.split()[0]

        elif label.find("ANT # / TYPE") != -1:
            string = line[0:20]
            if not string.split():
                sta.antno = ""
            else:
                sta.antno = string.split()[0]
            string = line[20:40]
            sta.antdes = string

        elif label.find("APPROX POSITION XYZ") != -1:
            j = 0
            for i in range(0, 3):
                sta.pos[i] = float(line[j:j+14])
                j = j+14
        elif label.find("ANTENNA: DELTA H/E/N") != -1:
            j = 0
            for i in range(0, 3):
                delt[i] = float(line[j:j+14])
                j = j+14
            sta.delt[0] = delt[1]
            sta.delt[1] = delt[2]
            sta.delt[2] = delt[0]
        elif label.find("ANTENNA: DELTA X/Y/Z") != -1:
            continue
        elif label.find("ANTENNA: PHASECENTER") != -1:
            continue
        elif label.find("ANTENNA: B.SIGHT XYZ") != -1:
            continue
        elif label.find("ANTENNA: ZERODIR AZI") != -1:
            continue
        elif label.find("ANTENNA: ZERODIR XYZ") != -1:
            continue
        elif label.find("CENTER OF MASS: XYZ") != -1:
            continue
        elif label.find("SYS / # / OBS TYPES") != -1:  # ver 3.0
            syscode = line[0]
            if syscode == "G":
                i = glc().SYS_GPS
            elif syscode == "R":
                i = glc().SYS_GLO
            elif syscode == "E":
                i = glc().SYS_GAL
            elif syscode == "C":
                i = glc().SYS_BDS
            elif syscode == "J":
                i = glc().SYS_QZS
            else:
                continue
            n = int(line[3:7])
            k = 6
            nt = 0
            for j in range(n):
                if k > 58:
                    k = 7
                string = line[k+1:k+3]
                tobs[nt, :, i] = string
                nt = nt+1
                k = k+4
            if i == 4 and (headinfo.ver-3.02) < 1e-3:
                for j in range(nt):
                    if tobs[j, 2, i] == "1":
                        tobs[j, 2, i] == "2"

        elif label.find("WAVELENGTH FACT L1/2") != -1:
            continue
        elif label.find("# / TYPES OF OBSERV") != -1:  # ver 2.0
            n = float(line[0:7])
            j = 9
            nt = 0
            for i in range(n):
                if j > 58:
                    j = 9
                if headinfo.ver <= 2.99:
                    string = line[j+1:j+2]
                    idx = find_str(string, " ")
                    string[idx[-1]+1:-1] = ""
                    tobs[nt, :, 0] = convcode(
                        headinfo.ver, string, glc().SYS_GPS)
                    tobs[nt, :, 1] = convcode(
                        headinfo.ver, string, glc().SYS_GLO)
                    tobs[nt, :, 2] = convcode(
                        headinfo.ver, string, glc().SYS_GAL)
                    tobs[nt, :, 3] = convcode(
                        headinfo.ver, string, glc().SYS_BDS)
                    tobs[nt, :, 4] = convcode(
                        headinfo.ver, string, glc().SYS_QZS)
                nt = nt+1
                j = j+6

        elif label.find("SIGNAL STRENGTH UNIT") != -1:
            continue
        elif label.find("INTERVAL") != -1:
            continue
        elif label.find("TIME OF FIRST OBS") != -1:
            if line[48:51] == "GPS":
                headinfo.tsys = glc().TSYS_GPS
            elif line[48:51] == "GLO":
                headinfo.tsys = glc().TSYS_GLO
            elif line[48:51] == "GAL":
                headinfo.tsys = glc().TSYS_GAL
            elif line[48:51] == "BDT":
                headinfo.tsys = glc().TSYS_BDS
            elif line[48:51] == "QZS":
                headinfo.ver = glc().TSYS_QZS

        elif label.find("TIME OF LAST OBS") != -1:
            continue
        elif label.find("RCV CLOCK OFFS APPL") != -1:
            continue
        elif label.find("SYS / DCBS APPLIED") != -1:
            continue
        elif label.find("SYS / PCVS APPLIED") != -1:
            continue
        elif label.find("SYS / SCALE FACTOR") != -1:
            continue
        elif label.find("SYS / PHASE SHIFTS") != -1:
            continue
        elif label.find("GLONASS SLOT / FRQ #") != -1:
            p = 4
            prn = 0
            for i in range(8):
                if not line[p+1:p+2]:
                    prn = float(line[p+1:p+2])
                if not line[p+5:p+6]:
                    fcn = float(line[p+5:p+6])
                if prn >= 1 and prn <= glc().MAXPRNGLO:
                    nav.glo_fcn[int(prn-1)] = fcn+8
                    p = p+7

        elif label.find("GLONASS COD/PHS/BIS") != -1:
            p = 0
            for i in range(4):
                if line[p+1:p+3] == "C1C":
                    nav.glo_cpbias[0] = float(line[p+4:p+12])
                elif line[p+1:p+3] == "C1P":
                    nav.glo_cpbias[1] = float(line[p+4:p+12])
                elif line[p+1:p+3] == "C2C":
                    nav.glo_cpbias[2] = float(line[p+4:p+12])
                elif line[p+1:p+3] == "C2P":
                    nav.glo_cpbias[3] = float(line[p+4:p+12])
                p = p+13

        elif label.find("LEAP SECONDS") != -1:
            nav.leaps = float(line[0:6])
        elif label.find("# OF SALTELLITES") != -1:
            continue
        elif label.find("PRN / # OF OBS") != -1:
            continue
        elif label.find("END OF HEADER") != -1:
            break
    
    obs.sta = sta
    decode_err = False
    
    return decode_err
