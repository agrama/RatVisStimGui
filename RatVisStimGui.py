if __name__ == "__main__":

    # from shared import Shared
    #
    # shared = Shared()
    # shared.start_threads()

    from PyQt5 import QtCore, QtGui, uic, QtWidgets
    import sys
    import os
    import pyqtgraph as pg
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
            self.exposure_slider.valueChanged[int].connect(self.exposure_slider_value_changed)
            # self.ImageView.image('test.jpg')
            self.pyqtgraph_image_item = pg.ImageItem(image=np.random.randint(0,255,(250, 250)))
            # self.ImageItem.hideAxis('left')
            # self.ImageItem.hideAxis('bottom')
            self.graphicsView.setAspectLocked(True)
            self.graphicsView.addItem(self.pyqtgraph_image_item)
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.updateData)
            self.timer.start(5)
            # updateData()
            # self.ImageItem.setImage(np.random.randint(0,255,(200,200)), autoLevels=False, levels=(0, 255))
        def pushButton_loadstim_clicked(self):
            full_path_to_module = os.path.abspath(QtWidgets.QFileDialog.getOpenFileName()[0])
            self.lineEdit_stimpath.setText(full_path_to_module)
        def pushButton_start_stim_clicked(self):
            None
        def exposure_slider_value_changed(self, value):
            self.exposure_slider_label.setText('Exposure = %d ms'%value)
        def updateData(self):
            self.pyqtgraph_image_item.setImage(np.random.randint(0,255,(250,250)))
            # None
    app = QtWidgets.QApplication(sys.argv)

    try:
        main_window = Main_Window()
        main_window.show()
        app.exec_()




    except:
        print("WTFFF")



