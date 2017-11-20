import pypylon as pp
from multiprocessing import Process
import numpy as np
import time
import tifffile as tiff

class CameraModule(Process):
    def __init__(self,shared):
        Process.__init__(self)
        self.shared = shared
    def run(self):
        camera_list = pp.factory.find_devices()
        print(camera_list)
        camera = pp.factory.create_device(camera_list[0])
        try:
            camera.open()
            print("Camera is opened")
        except:
            camera.close()
            print('could not open camera')
            self.shared.main_program_still_running.value = 0
        camera.properties['BinningHorizontalMode'] = 'Average'
        camera.properties['BinningVerticalMode'] = 'Average'
        camera.properties['Gain'] = 10
        camera.properties['BinningVertical'] = 4
        camera.properties['BinningHorizontal'] = 4
        self.shared.frame_width.value = camera.properties['Width']
        self.shared.frame_height.value = camera.properties['Height']
        camera.properties['ExposureTime'] = 1000
        self.shared.framerate.value = camera.properties['ResultingFrameRate']
        camera_generator = camera.grab_images(-1)
        while self.shared.main_program_still_running.value == 1:
            # print('wtf')
            if self.shared.camera_exposure_update_requested.value == 1:
                camera.properties['ExposureTime'] = self.shared.camera_exposure.value
                self.shared.framerate.value = camera.properties['ResultingFrameRate']
                self.shared.camera_exposure_update_requested.value = 0
            if self.shared.camera_gain_update_requested.value ==1:
                camera.properties['Gain'] = self.shared.camera_gain.value
                self.shared.camera_gain_update_requested.value = 0
            img = camera_generator.__next__()
            # img = camera.grab_image()
            data = img.flatten()
            self.shared.frame_len.value = len(data)
            self.shared.frame[:len(data)] = data
        camera.close()
        print('Camera is closed')


