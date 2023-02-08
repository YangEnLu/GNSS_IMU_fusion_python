from ..common.global_constants import glc, headinfo


def decode_rnxh(fname):
    fid = open(fname, "r")

    # Read the common part of the renix header information

    # default file header information
    head = headinfo()
    sys = glc().SYS_GPS
    tsys = glc().TSYS_GPS

    for line in fid:
        label = line[60:-1]
        if len(line) <= 60:
            continue
        elif label.find("RINEX VERSION / TYPE") != -1:
            # print(line)
            head.ver = float(line[0:9])
            head.type = line[20]
            if line[40] == "":
                pass
            elif line[40] == "G":
                sys = glc().SYS_GPS
                tsys = glc().TSYS_GPS
            elif line[40] == "R":
                sys = glc().SYS_GLO
                tsys = glc().TSYS_UTC
            elif line[40] == "E":
                sys = glc().SYS_GAL
                tsys = glc().TSYS_GAL
            elif line[40] == "C":
                sys = glc().SYS_BDS
                tsys = glc().TSYS_BDS
            elif line[40] == "J":
                sys = glc().SYS_QZS
                tsys = glc().TSYS_QZS
            elif line[40] == "M":
                sys = glc().SYS_NONE
                tsys = glc().TSYS_GPS
            else:
                print(f"not supported satellite system: {line[40]}")
            head.sys = sys
            head.tsys = tsys
    return head
