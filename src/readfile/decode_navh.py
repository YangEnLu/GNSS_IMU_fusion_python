from ..common.global_constants import nav
import numpy as np


def decode_navh(nav: nav, fname: str):
    fid = open(fname, "r")
    num_line = 0
    for line in fid:
        num_line = num_line+1
        label = line[60:-1]
        if label.find("ION ALPHA") != -1:  # ver 2.0
            j = 2
            for i in range(4):
                nav.ion_gps[0, i] = float(line[j:j+12])
                j = j+12
        elif label.find("ION BETA") != -1:
            j = 2
            for i in range(4):
                nav.ion_gps[0, i+4] = float(line[j:j+12])
                j = j+12
        elif label.find("DELTA-UTC: A0,A1,T,W") != -1:
            j = 3
            for i in range(2):
                nav.utc_gps[0, i] = float(line[j:j+19])
                j = j+19
            if i <= 3:
                ii = i+1
                for i in range(ii, 4):
                    nav.utc_gps[0, i] = float(line[j:j+9])
                    j = j+9
        elif label.find("IONOSPHERIC CORR") != -1:  # ver 3.0
            if line.find("GPSA") != -1:
                j = 5
                for i in range(4):
                    nav.ion_gps[0, i] = float(line[j:j+12])
                    j = j+12
            elif line.find("GPSB") != -1:
                j = 5
                for i in range(4):
                    nav.ion_gps[0, i+4] = float(line[j:j+12])
                    j = j+12
            elif line.find("GAL") != -1:
                j = 5
                for i in range(4):
                    nav.ion_gal[0, i] = float(line[j:j+12])
                    j = j+12
            elif line.find("BDSA") != -1:
                j = 5
                for i in range(4):
                    nav.ion_bds[0, i] = float(line[j:j+12])
                    j = j+12
            elif line.find("BDSB") != -1:
                j = 5
                for i in range(4):
                    nav.ion_bds[0, i+4] = float(line[j:j+12])
                    j = j+12
            elif line.find("QZSA") != -1:
                j = 5
                for i in range(4):
                    nav.ion_qzs[0, i] = float(line[j:j+12])
                    j = j+12
            elif line.find("QZSB") != -1:
                j = 5
                for i in range(4):
                    nav.ion_qzs[0, i+4] = float(line[j:j+12])
                    j = j+12

        elif label.find("TIME SYSTEM CORR") != -1:  # ver 3.0
            if line.find("GPUT") != -1:
                nav.utc_gps[0, 0] = float(line[5:22])
                nav.utc_gps[0, 1] = float(line[22:38])
                nav.utc_gps[0, 2] = float(line[38:45])
                nav.utc_gps[0, 3] = float(line[45:50])
            elif line.find("GLUT") != -1:
                nav.utc_glo[0, 0] = float(line[5:22])
                nav.utc_glo[0, 1] = float(line[22:38])
            elif line.find("GAUT") != -1:
                nav.utc_gal[0, 0] = float(line[5:22])
                nav.utc_gal[0, 1] = float(line[22:38])
                nav.utc_gal[0, 2] = float(line[38:45])
                nav.utc_gal[0, 3] = float(line[45:50])
            elif line.find("BDUT") != -1:
                nav.utc_bds[0, 0] = float(line[5:22])
                nav.utc_bds[0, 1] = float(line[22:38])
                nav.utc_bds[0, 2] = float(line[38:45])
                nav.utc_bds[0, 3] = float(line[45:50])
            elif line.find("QZUT") != -1:
                nav.utc_qzs[0, 0] = float(line[5:22])
                nav.utc_qzs[0, 1] = float(line[22:38])
                nav.utc_qzs[0, 2] = float(line[38:45])
                nav.utc_qzs[0, 3] = float(line[45:50])
        elif label.find("LEAP SECONDS") != -1:
            nav.leaps = float(line[0:7])
        elif label.find("END OF HEADER") != -1:
            break

    return nav, num_line
