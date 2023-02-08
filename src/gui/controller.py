from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from .GNSSIMU_UI import Ui_MainWindow
from ..common.global_constants import gls, glc
from ..readfile.decode_cfg import decode_cfg


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.opt = gls().default_opt
        self.file = gls().default_file
        self.cfg_filename = ""
        self.obsr_filename = ""
        self.obsb_filename = ""
        self.eph_filename = ""
        self.peph = ""
        self.pclk = ""
        self.imu = ""
        self.gui_flag = 0
        self.decodeerror = True
        self.setup_control()

    def setup_control(self):
        self.ui.Quit.clicked.connect(self.close_window)
        self.ui.Run.clicked.connect(self.Run)
        self.ui.config_button.clicked.connect(self.open_cfg_file)
        self.ui.obsr_button.clicked.connect(self.open_obsr_file)
        self.ui.eph_button.clicked.connect(self.open_eph_file)
        self.ui.obsb_button.clicked.connect(self.open_obsb_file)
        self.ui.peph_button.clicked.connect(self.open_peph_file)
        self.ui.pclk_button.clicked.connect(self.open_pclk_file)
        self.ui.imu_button.clicked.connect(self.open_imu_file)

    def open_cfg_file(self):
        cfg_filename, filetype = QFileDialog.getOpenFileName(
            self, "Open config file", "./conf", "*.ini")                 # start path
        if not cfg_filename:
            self.ui.config_line_edit.setText("configuration file(essential)")
            self.file.path = ""
        else:
            self.ui.config_line_edit.setText(cfg_filename)
            self.cfg_filename = cfg_filename
            # decode configuration file
            decodeerror = decode_cfg(self.opt, self.cfg_filename)
            self.decodeerror = decodeerror
            if self.decodeerror:
                self.gui_flag = 0
            else:
                # match required input file
                self.file.path = self.opt.filepath+glc().sep

    def open_obsr_file(self):
        if not self.file.path:
            pass
        else:
            obsr_filename, filetype = QFileDialog.getOpenFileName(
                self, "Open obsr file", self.file.path, "*.*O;;*.*o")                 # start path
            if not obsr_filename:
                self.ui.obsr_line_edit.setText("rover obs file(essential)")
                self.obsr_filename = ""
            else:
                self.ui.obsr_line_edit.setText(obsr_filename)
                self.obsr_filename = obsr_filename
                self.file.obsr = obsr_filename

    def open_obsb_file(self):
        if not self.file.path:
            pass
        else:
            obsb_filename, filetype = QFileDialog.getOpenFileName(
                self, "Open obsb file", self.file.path, "*.*O;;*.*o")                 # start path
            if not obsb_filename:
                self.ui.obsb_line_edit.setText("base obs file(optional)")
                self.obsb_filename = ""
            else:
                self.ui.obsb_line_edit.setText(obsb_filename)
                self.obsb_filename = obsb_filename
                self.file.obsb = obsb_filename

    def open_eph_file(self):
        if not self.file.path:
            pass
        else:
            eph_filename, filetype = QFileDialog.getOpenFileName(
                self, "Open ephemeris file",  self.file.path, "*.*n;;*.*p")                 # start path
            if not eph_filename:
                self.ui.eph_line_edit.setText(
                    "broadcast ephemeris file(essential)")
                self.eph_filename = ""
            else:
                self.ui.eph_line_edit.setText(eph_filename)
                self.eph_filename = eph_filename
                self.file.beph = eph_filename
                
    def open_peph_file(self):
        if not self.file.path:
            pass
        else:
            peph_filename, filetype = QFileDialog.getOpenFileName(
                self, "Open precise ephemeris file",  self.file.path, "*.*p")                 # start path
            if not peph_filename:
                self.ui.peph_line_edit.setText(
                    "precise ephemeris file (optional)")
                self.peph_filename = ""
            else:
                self.ui.peph_line_edit.setText(peph_filename)
                self.peph_filename = peph_filename
                self.file.sp3 = peph_filename
                
    def open_pclk_file(self):
        if not self.file.path:
            pass
        else:
            pclk_filename, filetype = QFileDialog.getOpenFileName(
                self, "Open precise clock file",  self.file.path, "*.clk")                 # start path
            if not pclk_filename:
                self.ui.pclk_line_edit.setText(
                    "precise clock file (optional)")
                self.peph_filename = ""
            else:
                self.ui.pclk_line_edit.setText(pclk_filename)
                self.pclk_filename = pclk_filename
                self.file.clk = pclk_filename
                
    def open_imu_file(self):
        if not self.file.path:
            pass
        else:
            imu_filename, filetype = QFileDialog.getOpenFileName(
                self, "Open imu file",  self.file.path, "*.csv")                 # start path
            if not imu_filename:
                self.ui.imu_line_edit.setText(
                    "precise clock file (optional)")
                self.imu_filename = ""
            else:
                self.ui.imu_line_edit.setText(imu_filename)
                self.imu_filename = imu_filename
                self.file.imu = imu_filename

    def close_window(self):
        self.gui_flag = 0
        self.close()

    def Run(self):
        if self.eph_filename == "" or self.cfg_filename == "" or self.obsr_filename == "":
            self.gui_flag = 0
        elif self.decodeerror:
            self.gui_flag = 0
        else:
            self.gui_flag = 1
            self.close()
