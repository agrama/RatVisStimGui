import pypylon as pp
from multiprocessing import Process
import os
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
        camera.properties['Gain'] = 1
        camera.properties['BinningVertical'] = 4
        camera.properties['BinningHorizontal'] = 4
        self.shared.frame_width.value = camera.properties['Width']
        self.shared.frame_height.value = camera.properties['Height']
        camera.properties['ExposureTime'] = 1000
        self.shared.framerate.value = camera.properties['ResultingFrameRate']
        stim_dict = {'Leftbar':0,'Rightbar':1,'Upbar':2,'Downbar':3} # for accessing trial number from shared variable
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
            if self.shared.start_exp.value == 1:
                stim_type = bytearray(self.shared.stim_type[:self.shared.stim_type_len.value]).decode()
                stim_trial_count = np.ctypeslib.as_array(self.shared.stim_trial_count)
                path_to_file = os.path.join(bytearray(self.shared.save_path[:self.shared.save_path_len.value]).decode(),
                           stim_type+ '_trial_' + str(stim_trial_count[stim_dict[stim_type]]+1) +'.tif')
                tif = tiff.TiffWriter(path_to_file, append=True)
                num_frames=np.ceil(self.shared.stim_trials.value*10*camera.properties['ResultingFrameRate'])
                self.shared.stim_on.value = 1
                first_time=time.time()
                for i in range(0,int(num_frames)):
                    img = camera_generator.__next__()
                    second_time = time.time()
                    tif.save(img)
                    # print(1/(second_time-first_time))
                    first_time = second_time
                self.shared.start_exp.value=0
                tif.close()
        camera.close()
        print('Camera is closed')



