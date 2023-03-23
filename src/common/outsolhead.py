from .global_constants import rtk, default_opt, obs, glc
from .time2epoch import time2epoch
from .str2time import str2time


def outsolhead(rtk: rtk, opt: default_opt, obsr: obs):
    solopt = opt.sol
    sep = " "
    str_vel = ""
    str_att = ""
    modes = ['SPP', 'PPD', 'PPK', 'PPS', 'PPP Kinematic', 'PPP Static', 'SPP/INS LC',
             'PPD/INS LC', 'PPK/INS LC', 'PPP/INS LC', 'SPP/INS TC', 'PPD/INS TC',
             'PPK/INS TC', 'PPP/INS TC']
    ionoopts = ['off', 'broadcast model', 'iono-free LC', 'estimation']
    tropopts = ['off', 'Saastamoinen model', 'ZTD estimation', 'ZTD+grid']

    # version
    string = f"% program   : {opt.ver}\n"

    # %% start and end time
    if opt.ts == glc().OPT_TS:
        time = obsr.data.item(0).time
        epoch = time2epoch(time)
    else:
        time = str2time(opt.ts)
        epoch = time2epoch(time)
    year = str(int(epoch[0]))
    if epoch[1] < 10:
        month = f"{0:d}{int(epoch[1]):d}"
    else:
        month = str(int(epoch[1]))
    if epoch[2] < 10:
        day = f"{0:d}{int(epoch[2]):d}"
    else:
        day = str(int(epoch[2]))
    if epoch[3] < 10:
        hour = f"{0:d}{int(epoch[3]):d}"
    else:
        hour = str(int(epoch[3]))
    if epoch[4] < 10:
        minute = f"{0:d}{int(epoch[4]):d}"
    else:
        minute = str(int(epoch[4]))
    if epoch[5] < 10:
        second = f"{0:d}{epoch[5]:.1f}"
    else:
        second = f"{epoch[5]:.1f}"

    string = string + \
        f"% obs start : {year:s}/{month:s}/{day:s} {hour:s}:{minute:s}:{second:s}\n"

    if opt.te == glc().OPT_TE:
        time = obsr.data[-1, 0].time
        epoch = time2epoch(time)
    else:
        time = str2time(opt.te)
        epoch = time2epoch(time)
    year = str(int(epoch[0]))
    if epoch[1] < 10:
        month = f"{0:d}{int(epoch[1]):d}"
    else:
        month = str(int(epoch[1]))
    if epoch[2] < 10:
        day = f"{0:d}{int(epoch[2]):d}"
    else:
        day = str(int(epoch[2]))
    if epoch[3] < 10:
        hour = f"{0:d}{int(epoch[3]):d}"
    else:
        hour = str(int(epoch[3]))
    if epoch[4] < 10:
        minute = f"{0:d}{int(epoch[4]):d}"
    else:
        minute = str(int(epoch[4]))
    if epoch[5] < 10:
        second = f"{0:d}{epoch[5]:.1f}"
    else:
        second = f"{epoch[5]:.1f}"

    string = string + \
        f"% obs end   : {year:s}/{month:s}/{day:s} {hour:s}:{minute:s}:{second:s}\n"

    # %% processing mode
    if opt.ins.mode == glc().GIMODE_OFF:
        # 'SPP', 'PPD', 'PPK', 'PPS', 'PPP Kinematic', 'PPP Static'
        mode = modes[int(opt.mode-1)]
    elif opt.ins.mode == glc().GIMODE_LC:
        if opt.mode == glc().PMODE_SPP:
            mode = modes[6]  # SPP/INS LC
        elif opt.mode == glc().PMODE_DGNSS:
            mode = modes[7]
        elif opt.mode == glc().PMODE_KINEMA:
            mode = modes[8]
        elif opt.mode == glc().PMODE_PPP_KINEMA:
            mode = modes[9]
    elif opt.ins.mode == glc().GIMODE_TC:
        if opt.mode == glc.PMODE_SPP:
            mode = modes[10]
        elif opt.mode == glc.PMODE_DGNSS:
            mode = modes[11]
        elif opt.mode == glc.PMODE_KINEMA:
            mode = modes[12]
        elif opt.mode == glc.PMODE_PPP_KINEMA:
            mode = modes[13]
    string = string+f"% mode      : {mode:s}\n"
    # %% navigation system
    str_sys = f"% system    : "
    if opt.navsys.find("G") != -1:
        str_sys = str_sys + "GPS "
    if opt.navsys.find("R") != -1:
        str_sys = str_sys + "GLONASS "
    if opt.navsys.find("E") != -1:
        str_sys = str_sys + "GALILEO "
    if opt.navsys.find("C") != -1:
        str_sys = str_sys + "BDS "
    if opt.navsys.find("J") != -1:
        str_sys = str_sys + "QZSS"
    string = string+f"{str_sys:s}\n"
    # %% number of frequencies
    string = string+f"% nfreqs    : {int(opt.nf):d}\n"
    # %% elevation mask
    string = string+f"% elev mask : {opt.elmin*glc().R2D:.1f} deg\n"
    # %% ephemeris
    if opt.sateph == glc().EPHOPT_BRDC:
        string = string+f"% ephemeris : broadcast\n"
    elif opt.sateph == glc().EPHOPT_PREC:
        string = string+f"% ephemeris : precise\n"
    # %% ionospheric
    ionoopt = ionoopts[int(opt.ionoopt)]
    string = string+f"% ionos opt : {ionoopt:s}\n"
    # %% tropspheric
    tropopt = tropopts[int(opt.tropopt)]
    string = string+f"% trops opt : {tropopt:s}\n"
    # %% write header to file
    string = string+"%"
    with open(rtk.outfile, "w") as fp:
        print(string, file=fp, end="\n")
    # %% write title to file
    if solopt.timef == glc().SOLT_GPST:
        gpst_str = "GPST"
        str_time = f"%  {gpst_str:<12}{sep:s}"
    elif solopt.timef == glc().SOLT_UTC:
        utc_str = "UTC"
        str_time = f"%  {utc_str:<20}{sep:s}"
    else:
        print("ERROR<outsolhead>: Time output options is wrong!!!")

    x_ecef = "x-ecef(m)"
    y_ecef = "y-ecef(m)"
    z_ecef = "z-ecef(m)"
    Q = "Q"
    ns = "ns"
    std_x = "sdx(m)"
    std_y = "sdy(m)"
    std_z = "sdz(m)"
    std_xy = "sdxy(m)"
    std_yz = "sdyz(m)"
    std_zx = "sdzx(m)"
    age = "age(s)"
    ratio = "ratio"
    vx = "vx(m/s)"
    vy = "vy(m/s)"
    vz = "vz(m/s)"
    std_vx = "sdvx"
    std_vy = "sdvy"
    std_vz = "sdvz"
    std_vxy = "sdvxy"
    std_vyz = "sdvyz"
    std_vzx = "sdvzx"
    lat = "latitude(deg)"
    lon = "longitude(deg)"
    h = "height(m)"
    std_e = "sde(m)"
    std_n = "sdn(m)"
    std_u = "sdu(m)"
    std_ne = "sdne(m)"
    std_eu = "sdeu(m)"
    std_un = "sdun(m)"
    vn = "vn(m/s)"
    ve = "ve(m/s)"
    vu = "vu(m/s)"
    std_vn = "sdvn"
    std_ve = "sdve"
    std_vu = "sdvu"
    std_vne = "sdvne"
    std_veu = "sdveu"
    std_vun = "sdvun"
    pitch = "pitch(deg)"
    roll = "roll(deg)"
    yaw = "yaw(deg)"
    std_p = "sdp"
    std_r = "sdr"
    std_y = "sdy"
    std_pr = "sdpr"
    std_ry = "sdry"
    std_yp = "sdyp"

    if solopt.posf == glc().SOLF_XYZ:
        str_pos = f"{x_ecef:>14}{sep:s}{y_ecef:>14}{sep:s}{z_ecef:>14}{sep:s}{Q:>3}{sep:s}{ns:>3s}{sep:s}{std_x:>8s}{sep:s}{std_y:>8s}{sep:s}{std_z:>8s}{sep:s}{std_xy:>8s}{sep:s}{std_yz:>8s}{sep:s}{std_zx:>8s}{sep:s}{age:>6s}{sep:s}{ratio:>6s}"
        if solopt.outvel == 1:
            str_vel = f"{sep:s}{vx:>10s}{sep:s}{vy:>10s}{sep:s}{vz:>10s}{sep:s}{std_vx:>9s}{sep:s}{std_vy:>8s}{sep:s}{std_vz:>8s}{sep:s}{std_vxy:>8s}{sep:s}{std_vyz:>8s}{sep:s}{std_vzx:>8s}"
    elif solopt.posf == glc().SOLF_LLH:
        str_pos = f"{lat:>14}{sep:s}{lon:>14}{sep:s}{h:>10}{sep:s}{Q:>3}{sep:s}{ns:>3s}{sep:s}{std_n:>8s}{sep:s}{std_e:>8s}{sep:s}{std_u:>8s}{sep:s}{std_ne:>8s}{sep:s}{std_eu:>8s}{sep:s}{std_un:>8s}{sep:s}{age:>6s}{sep:s}{ratio:>6s}"
        if solopt.outvel == 1:
            str_vel = f"{sep:s}{vn:>10s}{sep:s}{ve:>10s}{sep:s}{vu:>10s}{sep:s}{std_vn:>9s}{sep:s}{std_ve:>8s}{sep:s}{std_vu:>8s}{sep:s}{std_vne:>8s}{sep:s}{std_veu:>8s}{sep:s}{std_vun:>8s}"
    else:
        print("ERROR:<outsolhead> Position output options is wrong!!!")

    if solopt.outatt == 1:
        str_att = f"{sep:s}{pitch:>10s}{sep:s}{roll:>10s}{sep:s}{yaw:>10s}{sep:s}{std_p:>9s}{sep:s}{std_r:>8s}{sep:s}{std_y:>8s}{sep:s}{std_pr:>8s}{sep:s}{std_ry:>8s}{sep:s}{std_yp:>8s}"

    if opt.ins.mode == glc().GIMODE_OFF:
        string = str_time+str_pos
        if not str_vel == "":
            string = string+str_vel
    else:
        string = str_time+str_pos
        if not str_vel == "":
            string = string+str_vel
        if not str_att == "":
            string = string+str_att
        
    with open(rtk.outfile, "a") as fp:
        print(string, file=fp, end="\n")