from multiprocessing import Value, Array, Queue, sharedctypes
import ctypes
from CameraModule import CameraModule


class Shared():
    def __init__(self):
        self.main_program_still_running = Value("b", 1)

        self.camera_exposure = Value("i",1000)
        self.camera_exposure_update_requested = Value("b",0)
        self.camera_gain = Value('f',5.0)
        self.camera_gain_update_requested = Value('b',0)

        self.frame = sharedctypes.RawArray(ctypes.c_int8,500*500)
        self.frame_len = Value("i",0)
        self.frame_width = Value("i",200)
        self.frame_height = Value("i",200)
        self.framerate = Value("f",0)
    def start_threads(self):
        cameramodule = CameraModule(self)
        cameramodule.start()