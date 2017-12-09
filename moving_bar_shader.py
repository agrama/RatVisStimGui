from math import pi, sin, cos

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.DirectGui import *
import numpy as np
import sys

my_shader = [
            """#version 140

                    uniform mat4 p3d_ModelViewProjectionMatrix;
                    in vec4 p3d_Vertex;
                    in vec2 p3d_MultiTexCoord;
                    out vec2 texcoord;

                    void main() {
                      gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
                      texcoord = p3d_MultiTexCoord;
                    }
            """,

            """#version 140

                uniform sampler2D p3d_Texture0;
                in vec2 texcoord;
                out vec4 gl_FragColor;
                uniform float x_shift;
                uniform float y_shift;
                uniform float timer;

                void main() {

                 vec2 texcoord_translated = vec2(texcoord.x-x_shift , texcoord.y-y_shift);
                 vec4 color0 = texture(p3d_Texture0, texcoord_translated);
                 color0 = (color0-0.5)*sign(sin(2*3.14*timer*5)) +0.5;
                 gl_FragColor = color0;
               }
            """
            ]

loadPrcFileData("",
                """sync-video #f
                fullscreen #f
                win-origin 1920 0
                undecorated #t
                cursor-hidden #t
                win-size %d %d
                show-frame-rate-meter #f
                """ % (1920, 1920))

class MyApp(ShowBase):
    def __init__(self, shared):

        ShowBase.__init__(self)
        self.shared = shared
        self.disableMouse()
        self.accept('escape', self.escapeAction)
        self.winsize = 200
        self.x = 128*np.ones((self.winsize, self.winsize), dtype=np.uint8)
        self.barwidth = 8

        self.tex = Texture("texture")
        self.tex.setMagfilter(Texture.FTLinear)

        self.tex.setup2dTexture(self.winsize, self.winsize, Texture.TUnsignedByte, Texture.FLuminance)
        # memoryview(self.tex.modify_ram_image())[:] = x.astype(np.uint8).tobytes()


        cm = CardMaker('card')

        self.cardnode = self.render.attachNewNode(cm.generate())

        self.lens1 = PerspectiveLens()
        self.lens1.setNearFar(0.01, 100)
        self.lens1.setFov(90, 90)
        self.cam.node().setLens(self.lens1)

        self.cardnode.setPos(-0.5, 0.5, -0.5)

        self.cardnode.setTexture(self.tex)

        self.my_shader = Shader.make(Shader.SLGLSL, my_shader[0], my_shader[1])

        self.cardnode.setShader(self.my_shader)
        self.setBackgroundColor(0.5, 0.5, 0.5)
        self.cardnode.hide()

    def escapeAction(self):
        self.shared.main_programm_still_running.value = 0


