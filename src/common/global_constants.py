import numpy as np
import numpy.matlib as npm
import platform


class glc:
    def __init__(self):
        if platform.system() == "Windows":
            self.system = 0
            self.sep = "\\"
        elif platform.system() == "Linux":
            self.system = 1
            self.sep = "/"
        else:
            print("This program does not support this operating system!")

        self.PI = np.pi
        self.D2R = self.PI/180.0
        self.R2D = 180.0/self.PI
        self.CLIGHT = 299792458.0  # speed of light (m/s)
        self.SC2RAD = 3.1415926535898  # semi-circle to radian (IS-GPS)
        self.AU = 149597870691.0  # 1 AU(m)
        self.AS2R = self.D2R/3600.0  # arc sec to radian
        self.OMGE = 7.2921151467e-5  # earth angular velocity (IS-GPS) (rad/s)
        self.RE_WGS84 = 6378137.0  # earth semimajor axis (WGS84) (m)
        self.FE_WGS84 = 1.0/298.257223563  # earth flattening (WGS84)
        self.ECC_WGS84 = np.sqrt(
            2*self.FE_WGS84-self.FE_WGS84**2)  # earth eccentricity
        self.RP_WGS84 = (1-self.FE_WGS84)*self.RE_WGS84
        self.E1 = np.sqrt(self.RE_WGS84**2-self.RP_WGS84**2)/self.RE_WGS84
        self.E2 = np.sqrt(self.RE_WGS84**2-self.RP_WGS84**2)/self.RP_WGS84
        self.HION = 350000.0  # ionosphere height (m)
        ################## earth gravitational constant ###############
        self.MU_GPS = 3.9860050e14
        self.MU_GLO = 3.9860044e14
        self.MU_GAL = 3.986004418e14
        self.MU_BDS = 3.986004418e14
        ################## error factor ###############################
        self.EFACT_GPS = 1.0  # error factor: GPS
        self.EFACT_GLO = 1.5  # error factor: GLONASS
        self.EFACT_GAL = 1.0  # error factor: Galileo
        self.EFACT_BDS = 1.0  # error factor: BeiDou
        self.EFACT_QZS = 1.0  # error factor: QZSS
        ################## system number ###############################
        self.SYS_NONE = 0
        self.SYS_GPS = 1
        self.SYS_GLO = 2
        self.SYS_GAL = 3
        self.SYS_BDS = 4
        self.SYS_QZS = 5
        self.TSYS_GPS = 1
        self.TSYS_GLO = 2
        self.TSYS_GAL = 3
        self.TSYS_BDS = 4
        self.TSYS_QZS = 5
        self.TSYS_UTC = 6

        self.MINPRNGPS = 1  # min satellite PRN number of GPS
        self.MAXPRNGPS = 32  # max satellite PRN number of GPS
        # number of GPS satellites
        self.NSATGPS = (self.MAXPRNGPS-self.MINPRNGPS+1)
        self.NSYSGPS = 1

        self.MINPRNGLO = 1  # min satellite slot number of GLONASS
        self.MAXPRNGLO = 27  # max satellite slot number of GLONASS
        # number of GLONASS satellites
        self.NSATGLO = (self.MAXPRNGLO-self.MINPRNGLO+1)
        self.NSYSGLO = 1

        self.MINPRNGAL = 1  # min satellite PRN number of Galileo
        self.MAXPRNGAL = 36  # max satellite PRN number of Galileo
        # number of Galileo satellites
        self.NSATGAL = (self.MAXPRNGAL-self.MINPRNGAL+1)
        self.NSYSGAL = 1

        self.MINPRNBDS = 1  # min satellite sat number of BeiDou
        self.MAXPRNBDS = 45  # max satellite sat number of BeiDou
        # number of BeiDou satellites
        self.NSATBDS = (self.MAXPRNBDS-self.MINPRNBDS+1)
        self.NSYSBDS = 1

        self.MINPRNQZS = 193  # min satellite PRN number of QZSS
        self.MAXPRNQZS = 202  # max satellite PRN number of QZSS
        self.MINPRNQZS_S = 183  # min satellite PRN number of QZSS SAIF
        self.MAXPRNQZS_S = 191  # max satellite PRN number of QZSS SAIF
        # number of QZSS satellites
        self.NSATQZS = (self.MAXPRNQZS-self.MINPRNQZS+1)
        self.NSYSQZS = 1

        self.NSYS = self.NSYSGPS+self.NSYSGLO+self.NSYSGAL + \
            self.NSYSBDS+self.NSYSQZS  # number of systems
        self.MAXSAT = self.NSATGPS+self.NSATGLO+self.NSATGAL+self.NSATBDS+self.NSATQZS

        self.BD2_GEO = [1, 2, 3, 4, 5]
        self.BD2_IGSO = [6, 7, 8, 9, 10, 13, 16]
        self.BD2_MEO = [11, 12, 14]

        self.MAXOBSTYPE = 64  # max number of obs type in RINEX
        self.NFREQ = 3  # max used freq
        self.MAXFREQ = 6  # max freq for record
        self.NFREQGLO = 2
        self.MAXOBS = 128
        self.MAXRNXLEN = 16*self.MAXOBSTYPE+4
        self.MAXAGE = 30  # max age of differential between rover obs and base obs
        self.DTTOL = 0.025

        self.MAXDTOE = 7200.0  # max time difference to GPS Toe (s)
        self.MAXDTOE_QZS = 7200.0  # max time difference to QZSS Toe (s)
        self.MAXDTOE_GAL = 14400.0  # max time difference to Galileo Toe (s)
        self.MAXDTOE_BDS = 21600.0  # max time difference to BeiDou Toe (s)
        self.MAXDTOE_GLO = 1800.0  # max time difference to GLONASS Toe (s)
        self.MAXDTOE_SBS = 360.0  # max time difference to SBAS Toe (s)
        # max time difference to ephem toe (s) for other
        self.MAXDTOE_S = 86400.0
        self.MAXGDOP = 300.0  # max GDOP

        self.OPT_TS = '0000 00 00 00 00 00'     # default start time to process data
        self.OPT_TE = '0000 00 00 00 00 00'     # default end   time to process data

        self.PMODE_SPP = 1    # positioning mode: SPP
        self.PMODE_DGNSS = 2  # positioning mode: DGNSS
        self.PMODE_KINEMA = 3  # positioning mode: relative kinematic
        self.PMODE_STATIC = 4  # positioning mode: relative static
        self.PMODE_PPP_KINEMA = 5    # positioning mode: PPP-kinematic
        self.PMODE_PPP_STATIC = 6    # positioning mode: PPP-static

        self.SOLT_GPST = 1             # solution time: GPST
        self.SOLT_UTC = 2              # solution time: UTC
        self.SOLF_XYZ = 1              # solution format: x/y/z-ecef
        self.SOLF_LLH = 2              # solution format: lat/lon/height
        self.SOLQ_NONE = 0             # solution status: no solution
        self.SOLQ_FIX = 1              # solution status: fix
        self.SOLQ_FLOAT = 2            # solution status: float
        self.SOLQ_INS = 3              # solution status: pure INS
        self.SOLQ_DGNSS = 4            # solution status: DGNSS
        self.SOLQ_SPP = 5              # solution status: SPP
        self.SOLQ_PPP = 6              # solution status: PPP
        self.SOLQ_LC = 7               # solution status: GNSS/INS loosely coupled
        self.SOLQ_TC = 8               # solution status: GNSS/INS tightly coupled

        self.TIMES_GPST = 0                   # time system: gps time
        self.TIMES_UTC = 1                   # time system: utc
        self.TIMES_JST = 2                   # time system: jst

        self.IONOOPT_OFF = 0                   # ionosphere option: correction off
        self.IONOOPT_BRDC = 1                  # ionosphere option: broadcast model
        # ionosphere option: L1/L2 or L1/L5 iono-free LC
        self.IONOOPT_IFLC = 2
        self.IONOOPT_EST = 3                   # ionosphere option: estimation

        self.TROPOPT_OFF = 0                   # troposphere option: correction off
        self.TROPOPT_SAAS = 1                   # troposphere option: Saastamoinen model
        self.TROPOPT_EST = 2                   # troposphere option: ZTD estimation
        self.TROPOPT_ESTG = 3                   # troposphere option: ZTD+grad estimation

        self.EPHOPT_BRDC = 1                   # ephemeris option: broadcast ephemeris
        self.EPHOPT_PREC = 2                   # ephemeris option: precise ephemeris

        self.ARMODE_OFF = 0                   # AR mode: off
        self.ARMODE_CONT = 1                   # AR mode: continuous
        self.ARMODE_INST = 2                   # AR mode: instantaneous
        self.ARMODE_FIXHOLD = 3                # AR mode: fix and hold

        self.POSOPT_POS = 1                  # ref pos option: WGS84-XYZ
        self.POSOPT_SPP = 2                  # ref pos option: average of spp
        self.POSOPT_RINEX = 3                  # ref pos option: rinex header pos

        self.LAMBDA_ALL = 1                   # LAMBDA type: resolve all abmbiguity
        self.LAMBDA_PART = 2                   # LAMBDA type: resolve partial abmbiguity

        self.GLOICB_OFF = 0                   # GLONASS icb: off
        # GLONASS icb: linear function of frequency number
        self.GLOICB_LNF = 1
        # GLONASS icb: quadratic polynomial function of frequency number
        self.GLOICB_QUAD = 2

        self.AC_WUM = 1
        self.AC_GBM = 2
        self.AC_COM = 3

        self.GIMODE_OFF = 0                 # GNSS/INS mode: off
        self.GIMODE_LC = 1                # GNSS/INS mode: loosely couple
        self.GIMODE_TC = 2                # GNSS/INS mode: tightly couple

        self.MHZ_TO_HZ = 1000000.0
        self.FREQ_NONE = 0.0
        self.FREQ_GPS_L1 = 1575.42*self.MHZ_TO_HZ
        self.FREQ_GPS_L2 = 1227.60*self.MHZ_TO_HZ
        self.FREQ_GPS_L5 = 1176.45*self.MHZ_TO_HZ
        self.FREQ_GLO_G1 = 1602.00*self.MHZ_TO_HZ
        self.FREQ_GLO_G2 = 1246.00*self.MHZ_TO_HZ
        self.FREQ_GLO_G3 = 1202.025*self.MHZ_TO_HZ
        self.FREQ_GLO_D1 = 0.5625*self.MHZ_TO_HZ
        self.FREQ_GLO_D2 = 0.4375*self.MHZ_TO_HZ
        self.FREQ_GAL_E1 = 1575.42*self.MHZ_TO_HZ
        self.FREQ_GAL_E5A = 1176.45*self.MHZ_TO_HZ
        self.FREQ_GAL_E5B = 1207.140*self.MHZ_TO_HZ
        self.FREQ_GAL_E5AB = 1191.795*self.MHZ_TO_HZ
        self.FREQ_GAL_E6 = 1278.75*self.MHZ_TO_HZ
        self.FREQ_BDS_B1 = 1561.098*self.MHZ_TO_HZ
        self.FREQ_BDS_B2 = 1207.140*self.MHZ_TO_HZ
        self.FREQ_BDS_B3 = 1268.52*self.MHZ_TO_HZ
        self.FREQ_BDS_B1C = 1575.42*self.MHZ_TO_HZ
        self.FREQ_BDS_B2A = 1176.45*self.MHZ_TO_HZ
        self.FREQ_BDS_B2B = 1207.140*self.MHZ_TO_HZ
        self.FREQ_QZS_L1 = 1575.42*self.MHZ_TO_HZ
        self.FREQ_QZS_L2 = 1227.60*self.MHZ_TO_HZ
        self.FREQ_QZS_L5 = 1176.45*self.MHZ_TO_HZ
        self.FREQ_QZS_L6 = 1278.75*self.MHZ_TO_HZ

        self.CODE_NONE = 0
        self.CODE_L1C = 1
        self.CODE_L1S = 2
        self.CODE_L1L = 3
        self.CODE_L1X = 4
        self.CODE_L1P = 5
        self.CODE_L1W = 6
        self.CODE_L1Y = 7
        self.CODE_L1M = 8
        self.CODE_L1A = 9
        self.CODE_L1B = 10
        self.CODE_L1Z = 11
        self.CODE_L1D = 12
        self.CODE_L2C = 13
        self.CODE_L2D = 14
        self.CODE_L2S = 15
        self.CODE_L2L = 16
        self.CODE_L2X = 17
        self.CODE_L2P = 18
        self.CODE_L2W = 19
        self.CODE_L2Y = 20
        self.CODE_L2M = 21
        self.CODE_L2I = 22
        self.CODE_L2Q = 23
        self.CODE_L3I = 24
        self.CODE_L3Q = 25
        self.CODE_L3X = 26
        self.CODE_L4A = 27
        self.CODE_L4B = 28
        self.CODE_L4X = 29
        self.CODE_L5I = 30
        self.CODE_L5Q = 31
        self.CODE_L5X = 32
        self.CODE_L5D = 33
        self.CODE_L5P = 34
        self.CODE_L5Z = 35
        self.CODE_L6A = 36
        self.CODE_L6B = 37
        self.CODE_L6X = 38
        self.CODE_L6C = 39
        self.CODE_L6Z = 40
        self.CODE_L6S = 41
        self.CODE_L6L = 42
        self.CODE_L6E = 43
        self.CODE_L6I = 44
        self.CODE_L6Q = 45
        self.CODE_L7I = 46
        self.CODE_L7Q = 47
        self.CODE_L7X = 48
        self.CODE_L7D = 49
        self.CODE_L7P = 50
        self.CODE_L7Z = 51
        self.CODE_L8I = 52
        self.CODE_L8Q = 53
        self.CODE_L8X = 54
        self.CODE_L8D = 55
        self.CODE_L8P = 56
        self.CODE_L8Z = 57
        self.MAXCODE = 57

        self.obscodes = ['', '1C', '1S', '1L', '1X', '1P', '1W', '1Y', '1M', '1A',
                         '1B', '1Z', '1D', '2C', '2D', '2S', '2L', '2X', '2P', '2W',
                         '2Y', '2M', '2I', '2Q', '3I', '3Q', '3X', '4A', '4B', '4X',
                         '5I', '5Q', '5X', '5D', '5P', '5Z', '6A', '6B', '6X', '6C',
                         '6Z', '6S', '6L', '6E', '6I', '6Q', '7I', '7Q', '7X', '7D',
                         '7P', '7Z', '8I', '8Q', '8X', '8D', '8P', '8Z', ',']
        # GPS L1(1) L2(2) L5(5)
        self.GPSfreqband = [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                            0, 0, 0, 2, 2, 2, 2, 2, 2, 2,
                            2, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                            3, 3, 3, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # GLO G1(1) G2(2) G3(3) G1a(4) G2a(6)
        self.GLOfreqband = [0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
                            0, 0, 0, 2, 0, 0, 0, 0, 2, 0,
                            0, 0, 0, 0, 3, 3, 3, 4, 4, 4,
                            0, 0, 0, 0, 0, 0, 5, 5, 5, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.GALfreqband = [0, 1, 0, 0, 1, 0, 0, 0, 0, 1,
                            1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            2, 2, 2, 0, 0, 0, 5, 5, 5, 5,
                            5, 0, 0, 0, 0, 0, 3, 3, 3, 0,
                            0, 0, 4, 4, 4, 0, 0, 0, 0, 0]

        # BDS B1(2),B2(7),B3(6),B1C(1),B2a(5),B2b(7)
        self.BDSfreqband = [0, 0, 0, 0, 4, 4, 0, 0, 0, 4,
                            0, 0, 4, 0, 0, 0, 0, 1, 0, 0,
                            0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
                            0, 0, 5, 5, 5, 0, 3, 0, 3, 0,
                            0, 0, 0, 0, 3, 3, 2, 2, 2, 6,
                            6, 6, 0, 0, 0, 0, 0, 0, 0, 0]
        # QZS L1(1) L2(2) L5(5) L6(6)
        self.QZSfreqband = [0, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                            0, 1, 0, 0, 0, 2, 2, 2, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            3, 3, 3, 3, 3, 0, 0, 0, 4, 0,
                            4, 4, 4, 4, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.codepris = np.array([['CWPYMNSL', 'CWPYMNDSLX', 'IQX', '', '', ''],
                                  ['CP', 'CP', 'IQX', 'ABX', 'ABXP', ''],
                                  ['CABXZ', 'IQX',   'IQX',
                                      'IQX',    'CABXZ', ''],
                                  ['IQX', 'IQXA',   'IQX',
                                      'DPXA',    'DPX', 'DPZ'],
                                  ['CSLXZ', 'SLX',   'IQXDPZ',    'SLXEZ',    '', '']])

        self.GPS_C1CC2W = 1
        self.GPS_C1CC5Q = 2
        self.GPS_C1CC5X = 3
        self.GPS_C1WC2W = 4
        self.GPS_C1CC1W = 5
        self.GPS_C2CC2W = 6
        self.GPS_C2WC2S = 7
        self.GPS_C2WC2L = 8
        self.GPS_C2WC2X = 9
        self.GLO_C1CC2C = 1
        self.GLO_C1CC2P = 2
        self.GLO_C1PC2P = 3
        self.GLO_C1CC1P = 4
        self.GLO_C2CC2P = 5
        self.GAL_C1CC5Q = 1
        self.GAL_C1CC6C = 2
        self.GAL_C1CC7Q = 3
        self.GAL_C1CC8Q = 4
        self.GAL_C1XC5X = 5
        self.GAL_C1XC7X = 6
        self.GAL_C1XC8X = 7
        self.BD2_C2IC7I = 1
        self.BD2_C2IC6I = 2
        self.BD3_C1XC5X = 3
        self.BD3_C1PC5P = 4
        self.BD3_C1DC5D = 5
        self.BD3_C1XC6I = 6
        self.BD3_C1PC6I = 7
        self.BD3_C1DC6I = 8
        self.BD3_C2IC6I = 9
        self.BD3_C1XC7Z = 10
        self.BD3_C1XC8X = 11
        self.QZS_C1CC2L = 1
        self.QZS_C1CC5X = 2
        self.QZS_C1CC5Q = 3
        self.QZS_C1XC2X = 4
        self.QZS_C1XC5X = 5
        self.QZS_C1CC1X = 6

        self.MAXDCBPAIR = 12
        self.DCBPAIR = [['C1C-C2W', 'C1C-C5Q', 'C1C-C5X', 'C1W-C2W', 'C1C-C1W', 'C2C-C2W', 'C2W-C2S', 'C2W-C2L', 'C2W-C2X', '', '', ''],
                        ['C1C-C2C', 'C1C-C2P', 'C1P-C2P', 'C1C-C1P',
                            'C2C-C2P', '', '', '', '', '', '', ''],
                        ['C1C-C5Q', 'C1C-C6C', 'C1C-C7Q', 'C1C-C8Q',
                            'C1X-C5X', 'C1X-C7X', 'C1X-C8X', '', '', '', '', ''],
                        ['C2I-C7I', 'C2I-C6I', 'C1X-C5X', 'C1P-C5P', 'C1D-C5D', 'C1X-C6I',
                         'C1P-C6I', 'C1D-C6I', 'C2I-C6I', 'C1X-C7Z', 'C1X-C8X', ''],
                        ['C1C-C2L', 'C1C-C5X', 'C1C-C5Q', 'C1X-C2X', 'C1X-C5X', 'C1C-C1X', '', '', '', '', '', '']]


class gtime:
    def __init__(self):
        self.time = 0.0
        self.sec = 0.0


class ftime:
    def __init__(self):
        self.ts = gtime()
        self.te = gtime()
        self.week = 0
        self.sow = 0
        self.year = 0
        self.doy = 0


class eph:
    def __init__(self):
        self.sat = 0
        self.iode = 0
        self.iodc = 0
        self.sva = 0
        self.svh = 0
        self.week = 0
        self.code = 0
        self.flag = 0
        self.toc = 0
        self.toe = 0
        self.ttr = 0
        self.A = 0
        self.e = 0
        self.i0 = 0
        self.OMG0 = 0
        self.omg = 0
        self.M0 = 0
        self.deln = 0
        self.OMGd = 0
        self.idot = 0
        self.crc = 0
        self.crs = 0
        self.cuc = 0
        self.cus = 0
        self.cic = 0
        self.cis = 0
        self.toes = 0
        self.fit = 0
        self.f0 = 0
        self.f1 = 0
        self.f2 = 0
        # GPS/QZS:tgd(1) P1/P2 GAL:tgd(1) E5a/E1 tgd(2) E5b/E1
        # BDS:tgd(1) B1/B3 tgd(2) B2/B3
        self.tgd = np.array([[0, 0, 0, 0]])
        self.Adot = 0
        self.ndot = 0


class geph:
    def __init__(self):
        self.sat = 0
        self.iode = 0
        self.frq = 0
        self.svh = 0
        self.sva = 0
        self.age = 0
        self.toe = 0
        self.tof = 0
        self.pos = np.zeros((3, 1))
        self.vel = np.zeros((3, 1))
        self.acc = np.zeros((3, 1))
        self.taun = 0
        self.gamn = 0
        self.dtaun = 0


class peph:
    def __init__(self):
        self.time = gtime()
        self.pos = np.zeros((glc().MAXSAT, 4))
        self.std = np.zeros((glc().MAXSAT, 4))
        self.vel = np.zeros((glc().MAXSAT, 4))
        self.vst = np.zeros((glc().MAXSAT, 4))
        self.cov = np.zeros((glc().MAXSAT, 3))
        self.vco = np.zeros((glc().MAXSAT, 3))


class pclk:
    def __init__(self):
        self.time = gtime()
        self.clk = np.zeros((glc().MAXSAT, 1))
        self.std = np.zeros((glc().MAXSAT, 1))


class erpd:
    def __init__(self):
        self.mjd = 0
        self.xp = 0
        self.yp = 0
        self.xpr = 0
        self.ypr = 0
        self.ut1_utc = 0
        self.lod = 0


class erp:
    def __init__(self):
        self.n = 0
        self.nmax = 0
        self.data = erpd()


class pcv:
    def __init__(self):
        self.sat = 0
        self.type = ""
        self.code = ""
        self.ts = gtime()
        self.te = gtime()
        self.off = np.zeros((5*glc().NFREQ, 3))
        self.var = np.zeros((5*glc().NFREQ, 80*20))
        self.dazi = 0
        self.zen1 = 0
        self.zen2 = 0
        self.dzen = 0


class pcvs:
    def __init__(self):
        self.n = 0


class sv:
    def __init__(self):
        self.svh = -1
        self.pos = np.zeros((3, 1))
        self.vel = np.zeros((3, 1))
        self.dts = 0
        self.dtsd = 0
        self.vars = 0


class ant_para:
    def __init__(self):
        self.n = 0


class nav:
    def __init__(self):
        self.n = 0
        self.nmax = 0
        self.ng = 0
        self.ngmax = 0
        self.np = 0
        self.nc = 0
        self.no_CODE_DCB = 1
        self.utc_gps = np.zeros((1, 4))
        self.utc_glo = np.zeros((1, 4))
        self.utc_gal = np.zeros((1, 4))
        self.utc_bds = np.zeros((1, 4))
        self.utc_qzs = np.zeros((1, 4))
        self.ion_gps = np.zeros((1, 4))
        self.ion_gal = np.zeros((1, 4))
        self.ion_bds = np.zeros((1, 4))
        self.ion_qzs = np.zeros((1, 4))
        self.leaps = 0
        self.lam = np.zeros((glc().MAXSAT, glc().MAXFREQ))
        self.cbias = np.zeros((glc().MAXSAT, glc().MAXDCBPAIR))
        self.rbias = np.zeros((2, 3))
        self.wlbias = np.zeros((glc().MAXSAT, 1))
        self.glo_cpbias = np.zeros((glc().MAXSAT, 1))
        self.glo_fcn = np.zeros((glc().MAXPRNGLO+1, 1))
        self.ant_para = ant_para()
        self.otlp = np.zeros((11, 6, 2))
        self.erp = erp()
        self.pcvs = npm.repmat(pcv(), glc().MAXSAT, 1)


class sta:
    def __init__(self):
        self.name = ''
        self.maker = ''
        self.recsno = ''
        self.rectype = ''
        self.recver = ''
        self.antnp = ''
        self.antno = ''
        self.antdes = ''
        self.deltype = 0
        self.pos = np.zeros((3, 1))
        self.delt = np.zeros((3, 1))

# obs_tmp data


class obs_tmp:
    def __init__(self):
        self.time = gtime()
        self.sat = 0
        self.P = np.zeros((glc().NFREQ, 1))
        self.L = np.zeros((glc().NFREQ, 1))
        self.D = np.zeros((glc().NFREQ, 1))
        self.S = np.zeros((glc().NFREQ, 1))
        self.LLI = np.zeros((glc().NFREQ, 1))
        self.code = np.zeros((glc().NFREQ, 1))


class obsd:
    def __init__(self):
        self.time = gtime()
        self.sat = 0
        self.P = np.zeros((glc().MAXFREQ, 1))
        self.L = np.zeros((glc().MAXFREQ, 1))
        self.D = np.zeros((glc().MAXFREQ, 1))
        self.S = np.zeros((glc().MAXFREQ, 1))
        self.LLI = np.zeros((glc().MAXFREQ, 1))
        self.code = np.zeros((glc().MAXFREQ, 1))


class obs:
    def __init__(self):
        self.n = 0
        self.nepoch = 0
        self.dt = 0
        self.idx = 0
        self.sta = sta()


class imud:
    def __init__(self):
        self.time = gtime()
        self.dw = np.zeros((1, 3))
        self.dv = np.zeros((1, 3))


class imu:
    def __init__(self):
        self.n = 0
        self.idx = 0


class sol:
    def __init__(self):
        self.time = gtime()
        self.stat = 0
        self.ns = 0
        self.pos = np.zeros((1, 3))
        self.posP = np.zeros((1, 6))
        self.dtr = np.zeros((1, glc().NSYS))
        self.dtrd = 0
        self.vel = np.zeros((1, 3))
        self.velP = np.zeros((1, 6))
        self.ratio = 0
        self.age = 0
        self.att = np.zeros((1, 3))
        self.attP = np.zeros((1, 6))


class ref:
    def __init__(self):
        self.week = 0
        self.sow = 0
        self.pos = np.zeros((1, 3))
        self.vel = np.zeros((1, 3))
        self.att = np.zeros((1, 3))


class rcv:
    def __init__(self):
        self.time = gtime()
        self.oldpos = np.zeros((1, 3))
        self.oldvel = np.zeros((1, 3))
        self.clkbias = 0
        self.clkdrift = 0

# satellite state


class sat:
    def __init__(self):
        self.sys = 0
        self.vs = 0
        self.azel = np.zeros((1, 2))
        self.resp = np.zeros((1, glc().NFREQ))
        self.resc = np.zeros((1, glc().NFREQ))
        self.vsat = np.zeros((1, glc().NFREQ))  # valid satellite flag
        self.snr = np.zeros((1, glc().NFREQ))  # signal strength
        # ambiguity fix flag (1:fix,2:float,3:hold)
        self.fix = np.zeros((1, glc().NFREQ))
        self.slip = np.zeros((1, glc().NFREQ))  # slip flag
        self.slipb = np.zeros((1, glc().NFREQ))  # base slip flag
        self.half = np.zeros((1, glc().NFREQ))  # half-cycle valid flag
        self.lock = np.zeros((1, glc().NFREQ))  # lock counter of phase
        self.outc = np.zeros((1, glc().NFREQ))  # obs outage counter of phase
        self.slipc = np.zeros((1, glc().NFREQ))  # cycle slip counter
        self.rejc = np.zeros((1, glc().NFREQ))  # reject counter
        self.gf = 0  # geometry-free phase combination L1-L2
        self.gf2 = 0  # geometry-free phase combination L1-L5
        self.mw = 0  # MW combination
        self.phw = 0  # phase windup (cycle)
        self.pt = npm.repmat(gtime(), 2, glc().NFREQ)
        self.ph = np.zeros((2, 3))


class rtk:
    def __init__(self):
        self.nx = 0
        self.na = 0  # number of fixed states
        self.tt = 0  # time difference between current and previous (s)
        self.x = 0  # float states
        self.P = 0  # float states covariance
        self.xa = 0  # fixed states(only include the desired solution)
        self.Pa = 0  # fixed states covariance
        self.nfix = 0  # number of continuous fixes of ambiguity
        self.ambc = 0  # ambibuity control
        self.sol = sol()  # solution
        self.oldsol = sol()
        self.rcv = rcv()
        self.sat = npm.repmat(sat(), 1, glc().MAXSAT)  # satellite status
        # observation for receiver clock jump repair(noly for GPS)
        self.obs_rcr = np.zeros((32, 4))
        self.clkjump = 0  # receiver clock jump


class ins:
    def __init__(self):
        self.mode = 0          # solution mode(0:off 1:LC 2:TC)
        # ins aid gnss(0:off 1:on)([1]ins-aid cycle slip detection [2]ins-aid robust estimation)
        self.aid = np.array([[0, 0]])
        self.data_format = 0   # imu data format (0:rate 1:increment)
        self.sample_rate = 100  # imu sample rate(Hz)
        self.lever = np.array([[0, 0, 0]])   # lever
        # [pitch roll yaw](in rad)
        self.init_att_unc = np.array([[1, 1, 3]])*glc().D2R
        self.init_vel_unc = np.array([[10, 10, 10]])  # [e n u](in m/s)
        self.init_pos_unc = np.array([[30, 30, 30]])  # [B L H](in m)
        self.init_bg_unc = 0  # (deg/h--->rad/s)
        self.init_ba_unc = 0  # (ug   --->m/s^2)
        self.psd_gyro = 0  # gyro noise PSD (deg/sqrt(h)--->rad^2/s)
        self.psd_acce = 0    # acce noise PSD (ug/sqrt(Hz)--->m^2/s^3)
        self.psd_bg = 0     # gyro bias random walk PSD (deg/h--->rad^2/s^3)
        self.psd_ba = 0      # acce bias random walk PSD (ug   --->m^2/s^5)


class default_file:
    def __init__(self):
        self.path = ""
        self.obsr = ""
        self.obsb = ""
        self.beph = ""
        self.sp3 = ""
        self.clk = ""
        self.atx = ""  # antenna file
        self.dcb = ["", "", ""]
        self.dcb_mgex = ""  # DCB for MGEX
        self.erp = ""  # earth rotation parameters file
        self.blq = ""  # ocean tide loading parameters file
        self.imu = ""


class out_sol:
    def __init__(self):
        self.timef = 1  # time format(1:GPST 2:UTC)
        # position format(1:ECEF-XYZ 2:LLH(latitude longitude height))
        self.posf = 1
        self.outvel = 0  # output velocity(0:off 1:on)
        # output attitude(0:off 1:on)(only for GNSS/INS integration mode)
        self.outatt = 0


class default_opt:
    def __init__(self):
        self.ver = "GNSS_IMU_fusion_v1"
        self.ts = glc().OPT_TS
        self.te = glc().OPT_TE
        self.ti = 0  # time interval
        # 1:SPP 2:PPD(post-processing differenced) 3:PPK 4:relative static 5:PPP_KINE 6:PPP_STATIC
        self.mode = 0
        # navigation system(G:GPS R:GLONASS E:GALILEO C:BDS J:QZSS)
        self.navsys = "G"
        self.nf = 1
        self.elmin = 10*glc().D2R  # elevation mask angle(rad)
        self.snrmask = 36
        # satellite ephemeris/clock (1:broadcast ephemeris,2:precise ephemeris)
        self.sateph = 1
        # ionosphere option  (0:off,1:broadcast model,2:L1/L2 iono-free LC,3:estimation)
        self.ionoopt = 1
        # troposphere option (0:off 1:Saastamoinen model,2:ZTD estimation,3:ZTD+grid)
        self.tropopt = 1
        self.dynamics = 0  # dynamics model (0:off,1:on)
        self.tidecorr = 0  # earth tide correction (0:off,1:on)

        # AR mode (0:off,1:continuous,2:instantaneous,3:fix and hold 4:ppp_ar)
        self.modear = 0
        self.glomodear = 0  # GLONASS AR mode (0:off 1:on 2:auto cal)
        self.bdsmodear = 0  # BDS AR mode (0:off 1:on)
        self.elmaskar = 0           # elevation mask of AR(rad)
        self.elmaskhold = 0           # elevation mask to hold ambiguity(rad)
        self.LAMBDAtype = 1           # LAMBDA algrithm (1:all AR 2:partial AR)
        # AR threshold ([1]ratio test of all AR [2]success rate threshold of partial AR)
        self.thresar = [3.0, 0.995]
        # specified the used frequency order for BDS-2 ([1]B1 [2]B2 [3]B3)
        self.bd2frq = [1, 3, 2]
        # specified the used frequency order for BDS-3 ([1]B1 [3]B3 [4]B1C [5]B2a [6]B2b)
        self.bd3frq = [1, 3, 4]
        # GLONASS inter-frequency code bias (0:off 1:linear 2:quadratic)
        self.gloicb = 0
        self.gnsproac = 1  # GNSS precise product AC (1:wum 2:gbm 3:com 4:grm)
        # positioning options (0:off 1:on)
        self.posopt = [0, 0, 0, 0, 0, 0, 0]
        # ([1]satellite PCV [2]receiver PCV
        # [3]phase wind up [4]reject GPS Block IIA
        # [5]RAIM FDE [6]handle day-boundary clock jump
        # [7]gravitational delay correct)
        self.maxout = 3  # obs outage count to reset ambiguity
        self.minlock = 5  # min lock count to fix ambiguity
        self.minfix = 5  # min fix count to hold ambiguity
        # number of filter iteration(only for relative positioning)
        self.niter = 1
        self.maxinno = 30.0        # reject threshold of innovation(m)
        self.maxgdop = 30.0        # reject threshold of gdop

        # reject threshold of cycle slip detection([1]GF(m) [2]MW(m) [3]Doppler Integration(cycle))
        self.csthres = [0.05, 0.15, 2]
        # process-noise std([1]bias,[2]iono [3]trop [4]acch [5]accv [6] pos)
        self.prn = [1e-4, 1E-3, 1E-4, 1E-1, 1E-2, 0]
        # initial-state std([1]bias,[2]iono [3]trop)
        self.std = [30, 0.03, 0.3]
        # satellite clock stability (sec/sec)
        self.sclkstab = 5e-12
        # code/phase error ratio ([1]freq1 [2]freq2 [3]freq3)
        self.eratio = [100, 100, 100]
        # measurement error factor([1]:reserved [2-4]:error factor a/b/c of phase (m)
        # [5]:doppler frequency(hz))
        self.err = [100, 0.003, 0.003, 0, 1]

        # anttenna type ([1]rover [2]base station //automatic matching using wildcard "*")
        self.anttype = ['*', '*']
        # the source of antenna delta (0:from obs 1:from opt)
        self.antdelsrc = 0
        # antenna delta (ENU in m)([1]rover [2]base station //not using wildcard "*")
        self.antdel = np.array([[0, 0, 0], [0, 0, 0]])
        # obtain the base station position(1:pos in options 2:average of SPP 3:rinex header)
        self.basepostype = 1
        self.basepos = np.zeros((3, 1))  # base station position
        # ins setting
        self.ins = ins()
        self.sol = out_sol()

        self.filepath = ''
        self.sitename = ''

    def show_info(self):
        print(f"version = {self.ver}")
        print(f"time start = {self.ts}")
        print(f"time end = {self.te}")
        print(f"time interval = {self.ti}")


class headinfo:
    def __init__(self):
        self.ver = 2.10
        self.type = ""
        self.sys = None
        self.tsys = None


class index:
    def __init__(self):
        self.n = 0
        self.frq = np.zeros((1, glc().MAXOBSTYPE))
        self.pos = np.zeros((1, glc().MAXOBSTYPE))
        self.pri = np.zeros((1, glc().MAXOBSTYPE))
        self.type = np.zeros((1, glc().MAXOBSTYPE))
        self.code = np.zeros((1, glc().MAXOBSTYPE))
        self.shift = np.zeros((1, glc().MAXOBSTYPE))


class gls:
    def __init__(self):
        self.gtime = gtime()
        self.eph = eph()
        self.geph = geph()
        self.peph = peph()
        self.pclk = pclk()
        self.erpd = erpd()
        self.erp = erp()
        self.pcv = pcv()
        self.pcvs = pcvs()
        self.sv = sv()
        self.nav = nav()
        self.sta = sta()
        self.obs_tmp = obs_tmp()
        self.obsd = obsd()
        self.obs = obs()
        self.imud = imud()
        self.imu = imu()
        self.sol = sol()
        self.ref = ref()
        self.rcv = rcv()
        self.sat = sat()
        self.rtk = rtk()
        self.default_file = default_file()
        self.default_opt = default_opt()
