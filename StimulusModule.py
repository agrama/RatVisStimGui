from multiprocessing import Process, Value, Array, Queue, sharedctypes
from moving_bar_shader import MyApp
import time
import numpy as np



class StimulusModule(Process):
    def __init__(self, shared):
        Process.__init__(self)

        self.shared = shared

    def run(self):

        self.myapp = MyApp(self.shared)
        stim_trial_count = np.zeros((4,1),dtype=np.uint)
        self.shared.stim_trial_count[:len(stim_trial_count)] = stim_trial_count.flatten()
        while self.shared.main_program_still_running.value == 1:
            self.stimcode = bytearray(self.shared.stim_type[:self.shared.stim_type_len.value]).decode()
            self.stimtime = self.shared.stim_trials.value*10
            if self.shared.stim_on.value ==1:
                if self.stimcode == 'Rightbar':
                    stim_trial_count[1]+=1
                    self.shared.stim_trial_count[:len(stim_trial_count)] = stim_trial_count.flatten()
                    self.myapp.x[:,0:self.myapp.barwidth] = 255
                    memoryview(self.myapp.tex.modify_ram_image())[:] = self.myapp.x.astype(np.uint8).tobytes()
                    self.stim_start_time = time.time()
                    self.last_time = time.time()
                    self.myapp.cardnode.show()
                    while self.last_time - self.stim_start_time < self.stimtime: # present for 200 sec
                        self.myapp.cardnode.setShaderInput("y_shift", 0)
                        self.myapp.cardnode.setShaderInput("x_shift", (self.last_time - self.stim_start_time) * 0.1) # shift bar at 0.1 Hz
                        self.myapp.taskMgr.step()
                        self.last_time = time.time()
                    self.myapp.x = np.zeros((self.myapp.winsize, self.myapp.winsize), dtype=np.uint8)
                elif self.stimcode == 'Leftbar':
                    stim_trial_count[0]+=1
                    self.shared.stim_trial_count[:len(stim_trial_count)] = stim_trial_count.flatten()
                    self.myapp.x[:,-self.myapp.barwidth:-1] = 255
                    memoryview(self.myapp.tex.modify_ram_image())[:] = self.myapp.x.astype(np.uint8).tobytes()
                    self.stim_start_time = time.time()
                    self.last_time = time.time()
                    self.myapp.cardnode.show()
                    while self.last_time - self.stim_start_time < self.stimtime:  # present for 200 sec
                        self.myapp.cardnode.setShaderInput("y_shift", 0)
                        self.myapp.cardnode.setShaderInput("x_shift", -(self.last_time - self.stim_start_time) * 0.1)  # shift bar at 0.1 Hz
                        self.myapp.taskMgr.step()
                        self.last_time = time.time()
                    self.myapp.x = np.zeros((self.myapp.winsize, self.myapp.winsize), dtype=np.uint8)
                elif self.stimcode == 'Upbar':
                    stim_trial_count[2]+=1
                    self.shared.stim_trial_count[:len(stim_trial_count)] = stim_trial_count.flatten()
                    self.myapp.x[0:self.myapp.barwidth, :] = 255
                    memoryview(self.myapp.tex.modify_ram_image())[:] = self.myapp.x.astype(np.uint8).tobytes()
                    self.stim_start_time = time.time()
                    self.last_time = time.time()
                    self.myapp.cardnode.show()
                    while self.last_time - self.stim_start_time < self.stimtime:  # present for 200 sec
                        self.myapp.cardnode.setShaderInput("y_shift", (self.last_time - self.stim_start_time) * 0.1)  # shift bar at 0.1 Hz
                        self.myapp.cardnode.setShaderInput("x_shift", 0)
                        self.myapp.taskMgr.step()
                        self.last_time = time.time()
                    self.myapp.x = np.zeros((self.myapp.winsize, self.myapp.winsize), dtype=np.uint8)
                elif self.stimcode == 'Downbar':
                    stim_trial_count[3]+=1
                    self.shared.stim_trial_count[:len(stim_trial_count)] = stim_trial_count.flatten()
                    self.myapp.x[-self.myapp.barwidth:-1, :] = 255
                    memoryview(self.myapp.tex.modify_ram_image())[:] = self.myapp.x.astype(np.uint8).tobytes()
                    self.stim_start_time = time.time()
                    self.last_time = time.time()
                    self.myapp.cardnode.show()
                    while self.last_time - self.stim_start_time < self.stimtime:  # present for 200 sec
                        self.myapp.cardnode.setShaderInput("y_shift", -(self.last_time - self.stim_start_time) * 0.1) # shift bar at 0.1 Hz
                        self.myapp.cardnode.setShaderInput("x_shift", 0)
                        self.myapp.taskMgr.step()
                        self.last_time = time.time()
                    self.myapp.x = np.zeros((self.myapp.winsize, self.myapp.winsize), dtype=np.uint8)
                self.shared.stim_on.value = 0
                self.myapp.cardnode.hide()
            self.myapp.taskMgr.step()  # main panda loop, needed for redrawing, etc.

        self.myapp.destroy()
