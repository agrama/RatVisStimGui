from multiprocessing import Value, Array, Queue, sharedctypes
import ctypes
from CameraModule import CameraModule
from StimulusModule import StimulusModule


class Shared():
    def __init__(self):
        self.main_program_still_running = Value("b", 1)
        ###inputs from GUI
        #camera input
        self.camera_exposure = Value("i", 1000)
        self.camera_exposure_update_requested = Value("b", 0)
        self.camera_gain = Value('f', 5.0)
        self.camera_gain_update_requested = Value('b', 0)
        #path input
        self.save_path = sharedctypes.RawArray(ctypes.c_ubyte, 2000)
        self.save_path_len = Value("i", 0)
        #stim input
        self.stim_type = sharedctypes.RawArray(ctypes.c_ubyte,500)
        self.stim_type_len = Value('i',0)
        self.stim_trials = Value('i',0)
        self.stim_trial_count = sharedctypes.RawArray(ctypes.c_ubyte,4)

        ### camera capture
        self.frame = sharedctypes.RawArray(ctypes.c_int8, 500*500)
        self.frame_len = Value("i", 0)
        self.frame_width = Value("i", 200)
        self.frame_height = Value("i", 200)
        self.framerate = Value("f", 0)

        ### stimulus stuff
        self.start_exp = Value('b',0)
        self.stim_on = Value('b',0)

    def start_threads(self):
        cameramodule = CameraModule(self)
        cameramodule.start()
        stimulusmodule = StimulusModule(self)
        stimulusmodule.start()