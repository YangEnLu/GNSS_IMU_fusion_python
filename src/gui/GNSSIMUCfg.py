from PyQt5 import QtWidgets
from .controller import MainWindow_controller
import sys

# if __name__ == '__main__':


def OpenUI():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    app.exec_()
    gui_flag = window.gui_flag
    # cfg_filename = window.cfg_filename
    opt = window.opt
    file = window.file
    return opt, file, gui_flag
