if __name__ == "__main__":

    from shared import Shared
    import time
    shared = Shared()
    shared.start_threads()
    # time.sleep(10)
    from PyQt5 import QtCore, QtGui, uic, QtWidgets
    import sys
    import os
    import pyqtgraph as pg
    import numpy as np
    import pickle

    class Main_Window(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            self.shared = shared
            self.initUI()
        def initUI(self):
            # self.show()
            path = os.path.dirname(__file__)
            uic.loadUi(os.path.join(path, "Stim_Loader.ui"), self)

            self.filepath_pushButton.clicked.connect(self.filepath_pushButton_clicked)
            self.startStim_pushButton.clicked.connect(self.startStim_pushButton_clicked)

            ### change exposure and gain
            self.exposure_slider.valueChanged[int].connect(self.exposure_slider_value_changed)
            self.gain_slider.valueChanged[int].connect(self.gain_slider_value_changed)

            # self.ImageView.image('test.jpg')
            self.pyqtgraph_image_item = pg.ImageItem(image=np.random.randint(0,255,(250, 250)))
            # self.graphicsView.setAspectLocked(True)
            self.pyqtgraph_image_item.setAutoDownsample(True)
            # self.pyqtgraph_image_item.setScaledMode(2)
            self.viewRect = self.graphicsView.viewRect()
            print(self.viewRect)
            # self.pyqtgraph_image_item.setRect(self.viewRect)
            self.graphicsView.addItem(self.pyqtgraph_image_item)
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.updateData)
            self.timer.start(50)
            # updateData()
            # self.ImageItem.setImage(np.random.randint(0,255,(200,200)), autoLevels=False, levels=(0, 255))
        def filepath_pushButton_clicked(self):
            full_path_to_module = os.path.abspath(QtWidgets.QFileDialog.getOpenFileName()[0])
            self.savedirector_lineEdit.setText(full_path_to_module)
        def startStim_pushButton_clicked(self):
            None
        def exposure_slider_value_changed(self,value):
            self.exposure_slider_label.setText('Exposure = %d ms'%(value))
            self.framerate_label.setText('Frame rate = %.2f Hz'%self.shared.framerate.value)
            self.shared.camera_exposure.value = value
            self.shared.camera_exposure_update_requested.value = 1
        def gain_slider_value_changed(self,value):
            self.gain_slider_label.setText('Gain = %f'%(value/100))
            self.shared.camera_gain.value = value/100
            self.shared.camera_gain_update_requested.value = 1

        def updateData(self):
            frame = self.shared.frame
            frame = np.ctypeslib.as_array(self.shared.frame)[:self.shared.frame_len.value]
            if len(frame)>0:
                frame = frame.reshape((self.shared.frame_height.value,self.shared.frame_width.value))
                self.pyqtgraph_image_item.setImage(frame.T,autoLevels=False)
                self.pyqtgraph_image_item.setRect(self.viewRect)
            # None
        def closeEvent(self, a0: QtGui.QCloseEvent):
            self.shared.main_program_still_running.value = 0
            self.close()
    app = QtWidgets.QApplication(sys.argv)

    try:
        main_window = Main_Window()
        main_window.show()
        app.exec_()
    except:
        shared.main_program_still_running.value = 0
        print("WTFFF")



