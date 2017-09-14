if __name__ == "__main__":

    # from shared import Shared
    #
    # shared = Shared()
    # shared.start_threads()

    from PyQt5 import QtCore, QtGui, uic, QtWidgets
    import sys
    import os
    import numpy as np
    import pickle

    class Main_Window(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            self.initUI()
        def initUI(self):
            # self.show()
            path = os.path.dirname(__file__)
            uic.loadUi(os.path.join(path, "Stim_Loader.ui"), self)
            self.pushButton_loadstim.clicked.connect(self.pushButton_loadstim_clicked)
            self.pushButton_start_stim.clicked.connect(self.pushButton_start_stim_clicked)

        def pushButton_loadstim_clicked(self):
            full_path_to_module = os.path.abspath(QtWidgets.QFileDialog.getOpenFileName()[0])
            self.lineEdit_stimpath.setText(full_path_to_module)
        def pushButton_start_stim_clicked(self):
            None

    app = QtWidgets.QApplication(sys.argv)

    try:
        main_window = Main_Window()
        main_window.show()
        app.exec_()
    except:
        print("WTFFF")



