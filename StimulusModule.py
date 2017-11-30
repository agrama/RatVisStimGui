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
            self.stimtime = self.shared.stim_repetitions.value*self.shared.inter_stim_frame_interval.value # the visual stimuli will be on for these many camera frames
            if self.shared.stim_on.value ==1:
                if self.stimcode == 'Rightbar':
                    stim_trial_count[1]+=1
                    self.shared.stim_trial_count[:len(stim_trial_count)] = stim_trial_count.flatten()
                    self.myapp.x[:,0:self.myapp.barwidth] = 255
                    memoryview(self.myapp.tex.modify_ram_image())[:] = self.myapp.x.astype(np.uint8).tobytes()
                    #wait for desired number of frames before starting stimulus
                    while self.shared.framenum.value < self.shared.waitframes.value:
                        self.myapp.taskMgr.step()
                    # self.stim_start_time = time.time()
                    # self.last_time = time.time()
                    self.myapp.cardnode.show()
                    while self.shared.framenum.value-self.shared.waitframes.value < self.stimtime:
                        self.myapp.cardnode.setShaderInput("y_shift", 0)
                        self.myapp.cardnode.setShaderInput("x_shift", (self.shared.framenum.value-self.shared.waitframes.value)/self.shared.inter_stim_frame_interval.value)
                        self.myapp.taskMgr.step()
                        # self.last_time = time.time()
                    self.myapp.x = np.zeros((self.myapp.winsize, self.myapp.winsize), dtype=np.uint8)
                elif self.stimcode == 'Leftbar':
                    stim_trial_count[0]+=1
                    self.shared.stim_trial_count[:len(stim_trial_count)] = stim_trial_count.flatten()
                    self.myapp.x[:,-self.myapp.barwidth:-1] = 255
                    memoryview(self.myapp.tex.modify_ram_image())[:] = self.myapp.x.astype(np.uint8).tobytes()
                    # wait for desired number of frames before starting stimulus
                    while self.shared.framenum.value < self.shared.waitframes.value:
                        self.myapp.taskMgr.step()
                    # self.stim_start_time = time.time()
                    # self.last_time = time.time()
                    self.myapp.cardnode.show()
                    while self.shared.framenum.value-self.shared.waitframes.value < self.stimtime:
                        self.myapp.cardnode.setShaderInput("y_shift", 0)
                        self.myapp.cardnode.setShaderInput("x_shift", -(self.shared.framenum.value-self.shared.waitframes.value)/self.shared.inter_stim_frame_interval.value)
                        self.myapp.taskMgr.step()
                        # self.last_time = time.time()
                    self.myapp.x = np.zeros((self.myapp.winsize, self.myapp.winsize), dtype=np.uint8)
                elif self.stimcode == 'Upbar':
                    stim_trial_count[2]+=1
                    self.shared.stim_trial_count[:len(stim_trial_count)] = stim_trial_count.flatten()
                    self.myapp.x[0:self.myapp.barwidth, :] = 255
                    memoryview(self.myapp.tex.modify_ram_image())[:] = self.myapp.x.astype(np.uint8).tobytes()
                    # wait for desired number of frames before starting stimulus
                    while self.shared.framenum.value < self.shared.waitframes.value:
                        self.myapp.taskMgr.step()
                    # self.stim_start_time = time.time()
                    # self.last_time = time.time()
                    self.myapp.cardnode.show()
                    while self.shared.framenum.value-self.shared.waitframes.value < self.stimtime:
                        self.myapp.cardnode.setShaderInput("y_shift", (self.shared.framenum.value-self.shared.waitframes.value)/self.shared.inter_stim_frame_interval.value)
                        self.myapp.cardnode.setShaderInput("x_shift", 0)
                        self.myapp.taskMgr.step()
                        # self.last_time = time.time()
                    self.myapp.x = np.zeros((self.myapp.winsize, self.myapp.winsize), dtype=np.uint8)
                elif self.stimcode == 'Downbar':
                    stim_trial_count[3]+=1
                    self.shared.stim_trial_count[:len(stim_trial_count)] = stim_trial_count.flatten()
                    self.myapp.x[-self.myapp.barwidth:-1, :] = 255
                    memoryview(self.myapp.tex.modify_ram_image())[:] = self.myapp.x.astype(np.uint8).tobytes()
                    # wait for desired number of frames before starting stimulus
                    while self.shared.framenum.value < self.shared.waitframes.value:
                        self.myapp.taskMgr.step()
                    # self.stim_start_time = time.time()
                    # self.last_time = time.time()
                    self.myapp.cardnode.show()
                    while self.shared.framenum.value-self.shared.waitframes.value < self.stimtime:
                        self.myapp.cardnode.setShaderInput("y_shift", -(self.shared.framenum.value-self.shared.waitframes.value)/self.shared.inter_stim_frame_interval.value)
                        self.myapp.cardnode.setShaderInput("x_shift", 0)
                        self.myapp.taskMgr.step()
                        # self.last_time = time.time()
                    self.myapp.x = np.zeros((self.myapp.winsize, self.myapp.winsize), dtype=np.uint8)
                self.shared.stim_on.value = 0
                self.myapp.cardnode.hide()
            time.sleep(0.001)
            self.myapp.taskMgr.step()  # main panda loop, needed for redrawing, etc.

        self.myapp.destroy()
