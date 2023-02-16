from .global_constants import gtime
import math


def epoch2time(ep):
    time = gtime()
    time.time = 0
    time.sec = 0
    doy = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    year = ep[0]
    mon = ep[1]
    day = ep[2]
    if year < 1970 or year > 2099 or mon < 1 or mon > 12:
        return time
    if (year % 4 == 0) and mon>=3:
        temp = 1
    else:
        temp = 0
    days = (year-1970)*365+int((year-1969)/4)+doy[int(mon)-1]+day-2+temp
    sec = math.floor(ep[5])
    time.time = int(days*86400+ep[3]*3600+ep[4]*60+sec)
    time.sec = ep[5]-sec

    return time
