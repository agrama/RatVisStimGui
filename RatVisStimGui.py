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

            ### stimulus/stim params selector
            self.stim_comboBox.activated[str].connect(self.stim_comboBox_activated)
            self.startStim_pushButton.clicked.connect(self.startStim_pushButton_clicked)
            self.stim_repetitions_slider.valueChanged[int].connect(self.stim_repetitions_slider_value_changed)
            self.waitframes_spinBox.valueChanged[int].connect(self.waitframes_spinBox_value_changed)
            self.inter_stim_frame_interval_spinBox.valueChanged[int].connect(self.inter_stim_frame_interval_spinBox_value_changed)


            ### change exposure and gain
            self.exposure_spinBox.valueChanged[int].connect(self.exposure_spinBox_value_changed)
            self.gain_doubleSpinBox.valueChanged[float].connect(self.gain_doubleSpinBox_value_changed)

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
        def stim_repetitions_slider_value_changed(self,value):
            self.shared.stim_repetitions.value = value
            self.stim_repetitions_slider_label.setText('# stim repetitions = %d'%(value))
        def startStim_pushButton_clicked(self):
            self.shared.start_exp.value = 1
            self.startStim_pushButton.setStyleSheet('QPushButton{background-color: rgb(255, 43, 39);}')
        def waitframes_spinBox_value_changed(self,value):
            self.shared.waitframes.value = value
        def inter_stim_frame_interval_spinBox_value_changed(self,value):
            self.shared.inter_stim_frame_interval.value = value
            self.stim_frequency_label.setText('Stim Repetition Frequency (Hz) - %.3f'%(self.shared.framerate.value/value))
        def exposure_spinBox_value_changed(self,value):
            self.framerate_label.setText('Frame rate = %.2f Hz'%self.shared.framerate.value)
            self.stim_frequency_label.setText(
                'Stim Repetition Frequency (Hz) - %.3f' % (self.shared.framerate.value /self.shared.inter_stim_frame_interval.value))
            self.shared.camera_exposure.value = value
            self.shared.camera_exposure_update_requested.value = 1
        def gain_doubleSpinBox_value_changed(self,value):
            self.shared.camera_gain.value = value
            self.shared.camera_gain_update_requested.value = 1

        def updateData(self):
            stim_trial_count = np.ctypeslib.as_array(self.shared.stim_trial_count)
            # print(stim_trial_count)
            frame = np.ctypeslib.as_array(self.shared.frame)[:self.shared.frame_len.value]
            if len(frame)>0:
                frame = frame.reshape((self.shared.frame_height.value,self.shared.frame_width.value))
                frame=(255*(frame/4096.0)).astype(np.uint8)
                self.pyqtgraph_image_item.setImage(frame.T,autoLevels=False,autoDownsample=True)
                self.pyqtgraph_image_item.setRect(self.viewRect)
            self.stim_trial_label.setText('Leftbar: %d Rightbar: %d Upbar: %d Downbar: %d'
                                          % (stim_trial_count[0], stim_trial_count[1]
                                             , stim_trial_count[2], stim_trial_count[3]))
            if self.shared.start_exp.value ==0:
                self.startStim_pushButton.setStyleSheet('QPushButton{background-color: rgb(43, 255, 39);}')
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



