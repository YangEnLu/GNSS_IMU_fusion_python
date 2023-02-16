from ..common.global_constants import glc
import numpy as np


def decode_cfg(opt, fname: str) -> bool:
    decode_err = True
    fid = open(fname, "r")
    for line in fid:
        if line[0] == "#" or len(line) < 5:
            continue

        if line[0:13].find("data_dir") != -1:
            buff = line.split()
            opt.filepath = buff[2]
            continue

        if line[0:13].find("site_name") != -1:
            buff = line.split()
            opt.sitename = buff[2]
            continue

        if line[0:13].find("start_time") != -1:
            buff = line.split()
            time_opt = float(buff[2])
            if time_opt == 1:
                time1 = buff[3]
                time1 = time1.split("/")
                time1 = " ".join(time1)
                time2 = buff[4]
                time2 = time2.split(":")
                time2 = " ".join(time2)
                opt.ts = time1+" "+time2
                # for i, c in enumerate(time2):
                #     if c == ":":
                #         time2[i] = " "
                # time2 = "".join(time2)
            continue

        if line[0:13].find("end_time") != -1:
            buff = line.split()
            time_opt = float(buff[2])
            if time_opt == 1:
                time1 = buff[3]
                time1 = time1.split("/")
                time1 = " ".join(time1)
                time2 = buff[4]
                time2 = time2.split(":")
                time2 = " ".join(time2)
                opt.te = time1+" "+time2
            continue

        if line[0:13].find("t_interval") != -1:
            buff = line.split()
            opt.ti = float(buff[2])
            continue

        if line[0:13].find("gnss_mode") != -1:
            buff = line.split()
            opt.mode = float(buff[2])
            continue

        if line[0:13].find("navsys") != -1:
            buff = line.split()
            opt.navsys = buff[2]
            continue

        if line[0:13].find("nfreq") != -1:
            buff = line.split()
            opt.nfreq = float(buff[2])
            continue

        if line[0:13].find("elmin") != -1:
            buff = line.split()
            opt.elmin = float(buff[2])*glc().D2R
            continue

        if line[0:13].find("sateph") != -1:
            buff = line.split()
            opt.sateph = float(buff[2])
            continue

        if line[0:13].find("ionoopt") != -1:
            buff = line.split()
            opt.ionoopt = float(buff[2])
            continue

        if line[0:13].find("tropopt") != -1:
            buff = line.split()
            opt.tropopt = float(buff[2])
            continue

        if line[0:13].find("dynamics") != -1:
            buff = line.split()
            opt.dynamics = float(buff[2])
            continue

        if line[0:13].find("tidecorr") != -1:
            buff = line.split()
            opt.tidecorr = float(buff[2])
            continue

        if line[0:13].find("armode") != -1:
            buff = line.split()
            opt.modear = float(buff[2])
            continue

        if line[0:13].find("gloar") != -1:
            buff = line.split()
            opt.glomodear = float(buff[2])
            continue

        if line[0:13].find("bdsar") != -1:
            buff = line.split()
            opt.bdsmodear = float(buff[2])
            continue

        if line[0:13].find("elmaskar") != -1:
            buff = line.split()
            opt.elmaskar = float(buff[2])*glc().D2R
            continue

        if line[0:13].find("elmaskhold") != -1:
            buff = line.split()
            opt.elmaskhold = float(buff[2])*glc().D2R
            continue

        if line[0:13].find("LAMBDAtype") != -1:
            buff = line.split()
            opt.LAMBDAtype = float(buff[2])
            continue

        if line[0:13].find("thresar") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.thresar[0] = float(buff[0])
            opt.thresar[1] = float(buff[1])
            continue

        if line[0:13].find("bd2frq") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.bd2frq[0] = float(buff[0])
            opt.bd2frq[1] = float(buff[1])
            opt.bd2frq[2] = float(buff[2])
            continue

        if line[0:13].find("bd3frq") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.bd3frq[0] = float(buff[0])
            opt.bd3frq[1] = float(buff[1])
            opt.bd3frq[2] = float(buff[2])
            continue

        if line[0:13].find("gloicb") != -1:
            buff = line.split()
            opt.gloicb = float(buff[2])
            continue

        if line[0:13].find("gnsproac") != -1:
            buff = line.split()
            opt.gnsproac = float(buff[2])
            continue

        if line[0:13].find("posopt") != -1:
            line = line.split()
            buff = line[2]
            buff = buff.split(",")
            opt.posopt[0] = float(buff[0])
            opt.posopt[1] = float(buff[1])
            opt.posopt[2] = float(buff[2])
            opt.posopt[3] = float(buff[3])
            opt.posopt[4] = float(buff[4])
            opt.posopt[5] = float(buff[5])
            opt.posopt[6] = float(buff[6])
            continue

        if line[0:13].find("maxout") != -1:
            buff = line.split()
            opt.maxout = float(buff[2])
            continue

        if line[0:13].find("minlock") != -1:
            opt.minlock = float(line.split()[2])
            continue

        if line[0:13].find("minfix") != -1:
            opt.minfix = float(line.split()[2])
            continue

        if line[0:13].find("niter") != -1:
            opt.niter = float(line.split()[2])
            continue

        if line[0:13].find("maxinno") != -1:
            opt.maxinno = float(line.split()[2])
            continue

        if line[0:13].find("maxgdop") != -1:
            opt.maxgdop = float(line.split()[2])
            continue

        if line[0:13].find("csthres") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.csthres[0] = float(buff[0])
            opt.csthres[1] = float(buff[1])
            opt.csthres[2] = float(buff[2])
            continue

        if line[0:2].find("prn") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.prn[0] = float(buff[0])
            opt.prn[1] = float(buff[1])
            opt.prn[2] = float(buff[2])
            opt.prn[3] = float(buff[3])
            opt.prn[4] = float(buff[4])
            opt.prn[5] = float(buff[5])
            continue

        if line[0:2].find("std") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.std[0] = float(buff[0])
            opt.std[1] = float(buff[1])
            opt.std[2] = float(buff[2])
            continue

        if line[0:2].find("err") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.err[0] = float(buff[0])
            opt.err[1] = float(buff[1])
            opt.err[2] = float(buff[2])
            opt.err[3] = float(buff[3])
            opt.err[4] = float(buff[4])
            continue

        if line[0:13].find("sclkstab") != -1:
            opt.sclkstab = float(line.split()[2])
            continue

        if line[0:13].find("eratio") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.eratio[0] = float(buff[0])
            opt.eratio[1] = float(buff[1])
            opt.eratio[2] = float(buff[2])
            continue

        if line[0:13].find("antdelsrc") != -1:
            opt.antdelsrc = float(line.split()[2])
            continue

        if line[0:13].find("antdel") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.antdel = np.array([[0, 0, 0], [0, 0, 0]])
            opt.antdel[0, 0] = float(buff[0])
            opt.antdel[0, 1] = float(buff[1])
            opt.antdel[0, 2] = float(buff[2])
            opt.antdel[1, 0] = float(buff[3])
            opt.antdel[1, 1] = float(buff[4])
            opt.antdel[1, 2] = float(buff[5])
            continue

        if line[0:13].find("basepostype") != -1:
            opt.basepostype = float(line.split()[2])
            continue

        if line[0:13].find("baserefpos") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.basepos[0] = float(buff[0])
            opt.basepos[1] = float(buff[1])
            opt.basepos[2] = float(buff[2])
            continue
        
        if line[0:13].find("ins_mode") != -1:
            opt.ins.mode = float(line.split()[2])
            continue
        
        if line[0:13].find("ins_aid") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.ins.aid[0,0] = float(buff[0])
            opt.ins.aid[0,1] = float(buff[1])
            continue
        
        if line[0:13].find("data_format") != -1:
            opt.ins.data_format = float(line.split()[2])
            continue
        
        if line[0:13].find("sample_rate") != -1:
            opt.ins.sample_rate = float(line.split()[2])
            continue
        
        if line[0:13].find("lever") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.ins.lever[0,0] = float(buff[0])
            opt.ins.lever[0,1] = float(buff[1])
            opt.ins.lever[0,2] = float(buff[2])
            continue
        
        if line[0:13].find("init_att_unc") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.ins.init_att_unc[0,0] = float(buff[0])*glc().D2R
            opt.ins.init_att_unc[0,1] = float(buff[1])*glc().D2R
            opt.ins.init_att_unc[0,2] = float(buff[2])*glc().D2R
            continue
        
        if line[0:13].find("init_vel_unc") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.ins.init_vel_unc[0,0] = float(buff[0])
            opt.ins.init_vel_unc[0,1] = float(buff[1])
            opt.ins.init_vel_unc[0,2] = float(buff[2])
            continue
        
        if line[0:13].find("init_pos_unc") != -1:
            line = line.split()[2]
            buff = line.split(",")
            opt.ins.init_pos_unc[0,0] = float(buff[0])/glc().RE_WGS84
            opt.ins.init_pos_unc[0,1] = float(buff[1])/glc().RE_WGS84
            opt.ins.init_pos_unc[0,2] = float(buff[2])
            continue
        
        if line[0:13].find("init_bg_unc") != -1:
            opt.ins.init_bg_unc = float(line.split()[2])
            continue
        
        if line[0:13].find("init_ba_unc") != -1:
            opt.ins.init_ba_unc = float(line.split()[2])
            continue
        
        if line[0:13].find("psd_gyro") != -1:
            opt.ins.psd_gyro = float(line.split()[2])
            continue
        
        if line[0:13].find("psd_acce") != -1:
            opt.ins.psd_acce = float(line.split()[2])
            continue
        
        if line[0:13].find("psd_bg") != -1:
            opt.ins.psd_bg = float(line.split()[2])
            continue
        
        if line[0:13].find("psd_ba") != -1:
            opt.ins.psd_ba = float(line.split()[2])
            continue
        
        if line[0:13].find("timef") != -1:
            opt.sol.timef = float(line.split()[2])
            continue
        
        if line[0:13].find("posf") != -1:
            opt.sol.posf = float(line.split()[2])
            continue
        
        if line[0:13].find("outvel") != -1:
            opt.sol.outvel = float(line.split()[2])
            continue
        
        if line[0:13].find("outatt") != -1:
            opt.sol.outatt = float(line.split()[2])
            continue
        
    decode_err = False
    fid.close()
    return decode_err
