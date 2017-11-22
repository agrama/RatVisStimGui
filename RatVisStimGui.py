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

            ### enter directory to save and file name
            self.filepath_pushButton.clicked.connect(self.filepath_pushButton_clicked)
            self.file_path_lineEdit.textChanged.connect(self.file_path_lineEdit_textChanged)

            ### stimulus selector
            self.stim_comboBox.activated[str].connect(self.stim_comboBox_activated)
            self.startStim_pushButton.clicked.connect(self.startStim_pushButton_clicked)
            self.stim_trials_slider.valueChanged[int].connect(self.stim_trials_slider_value_changed)


            ### change exposure and gain
            self.exposure_slider.valueChanged[int].connect(self.exposure_slider_value_changed)
            self.gain_slider.valueChanged[int].connect(self.gain_slider_value_changed)

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
            # full_path_to_module = os.path.abspath(QtWidgets.QFileDialog.getOpenFileName()[0])
            full_path_to_directory = os.path.abspath(QtWidgets.QFileDialog.getExistingDirectory()).encode()
            self.shared.save_path_len.value = len(full_path_to_directory)
            self.shared.save_path[:self.shared.save_path_len.value]=full_path_to_directory
            self.file_path_lineEdit.setText(full_path_to_directory.decode())
        def file_path_lineEdit_textChanged(self):
            full_path_to_file = self.file_path_lineEdit.text().encode()
            self.shared.save_path_len.value = len(full_path_to_file)
            self.shared.save_path[:self.shared.save_path_len.value] = full_path_to_file

        def stim_comboBox_activated(self,text):
            text = text.encode()
            self.shared.stim_type_len.value = len(text)
            self.shared.stim_type[:self.shared.stim_type_len.value] = text
        def stim_trials_slider_value_changed(self,value):
            self.shared.stim_trials.value = value
            self.stim_trials_slider_label.setText('# trials = %d'%(value))
        def startStim_pushButton_clicked(self):
            self.shared.start_exp.value = 1
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
            stim_trial_count = np.ctypeslib.as_array(self.shared.stim_trial_count)
            # print(stim_trial_count)
            frame = np.ctypeslib.as_array(self.shared.frame)[:self.shared.frame_len.value]
            if len(frame)>0:
                frame = frame.reshape((self.shared.frame_height.value,self.shared.frame_width.value))
                self.pyqtgraph_image_item.setImage(frame.T,autoLevels=False)
                self.pyqtgraph_image_item.setRect(self.viewRect)
            self.stim_trial_label.setText('Leftbar: %d Rightbar: %d Upbar: %d Downbar: %d'
                                          % (stim_trial_count[0], stim_trial_count[1]
                                             , stim_trial_count[2], stim_trial_count[3]))
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



