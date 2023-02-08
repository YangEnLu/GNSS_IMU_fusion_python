from ..common.global_constants import glc


def convcode(ver, str, sys):
    type = "   "
    if str == "P1":
        if sys == glc().SYS_GPS:
            type = "C1W"
        if sys == glc().SYS_GLO:
            type = "C1P"
    elif str == "P2":
        if sys == glc().SYS_GPS:
            type = "C2W"
        if sys == glc().SYS_GLO:
            type = "C2P"
    elif str == "C1":
        if ver >= 2.12:
            pass
        elif sys == glc().SYS_GPS:
            type = "C1C"
        elif sys == glc().SYS_GLO:
            type = "C1C"
        elif sys == glc().SYS_GAL:
            type = "C1X"
        elif sys == glc().SYS_QZS:
            type = "C1C"
    elif str == "C2":
        if sys == glc().SYS_GPS:
            if ver >= 2.12:
                type = "C2W"
            else:
                type = "C2X"
        elif sys == glc().SYS_GLO:
            type = "C2C"
        elif sys == glc().SYS_BDS:
            type = "C1X"
        elif sys == glc().SYS_QZS:
            type = "C2X"
    elif ver >= 2.12 and str[1] == "A":
        if sys == glc().SYS_GPS:
            type = str[0]+"1C"
        elif sys == glc().SYS_GLO:
            type = str[0]+"1C"
        elif sys == glc().SYS_QZS:
            type = str[0]+"1C"
    elif ver >= 2.12 and str[1] == "B":
        if sys == glc().SYS_GPS:
            type = str[0]+"1X"
        elif sys == glc().SYS_QZS:
            type = str[0]+"1X"
    elif ver >= 2.12 and str[1] == "C":
        if sys == glc().SYS_GPS:
            type = str[0]+"2X"
        elif sys == glc().SYS_QZS:
            type = str[0]+"2X"
    elif ver >= 2.12 and str[1] == "D":
        if sys == glc().SYS_GLO:
            type = str[0]+"2C"
    elif ver >= 2.12 and str[1] == "1":
        if sys == glc().SYS_GPS:
            type = str[0]+"1W"
        elif sys == glc().SYS_GLO:
            type = str[0]+"1P"
        elif sys == glc().SYS_GAL:
            type = str[0]+"1X"
        elif sys == glc().SYS_BDS:
            type = str[0]+"1X"
    elif ver < 2.12 and str[1] == "1":
        if sys == glc().SYS_GPS:
            type = str[0]+"1C"
        elif sys == glc().SYS_GLO:
            type = str[0]+"1C"
        elif sys == glc().SYS_GAL:
            type = str[0]+"1X"
        elif sys == glc().SYS_QZS:
            type = str[0]+"1C"
    elif str[1]=="2":
        if sys==glc().SYS_GPS:
            type=str[0]+"2W"
        elif sys==glc().SYS_GLO:
            type=str[0]+"2P"
        elif sys==glc().SYS_BDS:
            type=str[0]+"1X"
        elif sys==glc().SYS_QZS:
            type=str[0]+"2X"
    elif str[1]=="5":
        if sys==glc().SYS_GPS:
            type=str[0]+"5X"
        elif sys==glc().SYS_GAL:
            type=str[0]+"5X"
        elif sys==glc().SYS_QZS:
            type=str[0]+"5X" 
    elif str[1]=="6":
        if sys==glc().SYS_GAL:
            type=str[0]+"6X"
        elif sys==glc().SYS_BDS:
            type=str[0]+"6X"
        elif sys==glc().SYS_QZS:
            type=str[0]+"6X"
    elif str[1]=="7":
        if sys==glc().SYS_GAL:
            type=str[0]+"7X"
        elif sys==glc().SYS_BDS:
            type = str[0]+"7X"
    elif str[1]=="8":
        if sys==glc().SYS_GAL:
            type=str[0]+"8X"
    
    return type
