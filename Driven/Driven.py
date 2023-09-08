from color_seperate import ColorSeperate
from pop.Pilot import Object_Follow, Camera, SerBot
from lidar import Lidar
from threading import Thread
import time
import sys

class Driven(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance"):
            cls.__instance = super().__new__(cls)
            return cls.__instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "__init"):
            self.cam = None
            
            self.of = None
            self.human_x = None

            self.colorS = None
            self.bot = None
            self.bot_speed = 50

            self.lidar = None
            self.length = [1000, 400, 200]   # 측정 거리
            self.lidar_detect = 3

            self.loaded = False
            self.run_pause = False

            self.run_t = None

            cls.__init = True

    def __del__(self):
        del self.lidar
        del self.bot
        del self.colorS
        del self.of
        del self.cam

    def load(self):
        if not self.loaded:
            self.bot = SerBot()
            self.bot.setSpeed(self.bot_speed)
            self.lidar = Lidar(self.length)
            print("[SerBot] : === Bot, Lidar Setting Complete ===") 

            self.cam = Camera(320,320)
            self.of = Object_Follow(self.cam)
            self.of.load_model()
            print("[SerBot] : === Object Follow Module Loaded Complete ===")
            self.colorS = ColorSeperate(self.cam)
            
            self.run_t = Thread(target=self.run, daemon=True)
            self.run_t.start()
            print("[SerBot] : === Running. ===")

            self.loaded = True
        else :
            print("[SerBot] : Already Loaded")

    def human_detect(self):
        person = self.of.detect(index='person')
        if person:
            self.human_x = round(person['x'] * 4, 1)

            self.bot_speed = 90 if self.lidar_detect == 0 else 60 if self.lidar_detect == 1 else 30
            # self.bot.setSpeed(self.bot_speed)
        else: 
            self.human_x = None
            self.bot.stop()

    def run(self):
        while True:
            # print("[SerBot] : Lidar Scanning")
            if not self.run_pause :
                self.lidar_detect = self.lidar.check_distance(self.bot.steering)

                if self.lidar_detect != 3 :
                    self.human_detect()
                    if self.colorS.x_cor and self.human_x :
                        hum_x = self.human_x
                        cols_x = self.colorS.x_cor
                        if hum_x >= cols_x - 0.05 and hum_x <= cols_x + 0.05 :
                            x = hum_x
                        else :
                            x = round(cols_x*4, 1)
                        self.bot.steering = 1.0 if x > 1.0 else -1.0 if x < -1.0 else x
                        self.bot.forward()
                    else:
                        self.bot.stop()
                else:
                    self.bot.stop()

    def pause(self, state):
        if state:
            self.lidar.pause(True)
            self.bot.stop()
            self.run_pause = True
        else:
            self.lidar.pause(False)
            self.run_pause = False


if __name__ == '__main__' :
    try:
        drv = Driven()
        drv.load()

        while True:
            i = input()
            if i == 'T':
                drv.pause(True)
            elif i == 'F':
                drv.pause(False)
            else:
                print("What?")
    except KeyboardInterrupt:
        sys.exit()
