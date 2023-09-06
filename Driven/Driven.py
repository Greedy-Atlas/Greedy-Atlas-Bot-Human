from .color_seperate import ColorSeperate
from pop.Pilot import Object_Follow, Camera, SerBot
from lidar import Lidar
import time

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

            self.lidar = None
            self.length = [800, 400, 200]   # 측정 거리
            self.lidar_detect = 3

            self.loaded = False
            cls.__init = True

    def load(self):
        if not self.loaded:
            self.bot = SerBot()
            self.lidar = Lidar()
            self.cam = Camera(320,320)
            self.of = Object_Follow(self.cam)
            self.of.load_model()
            print("[SerBot] : === Loaded Complete ===")
            self.colorS = ColorSeperate(self.cam)
            
            self.loaded = True
        else :
            print("[SerBot] : Already Loaded")

    def human_detect(self):
        person = self.of.detect(index='person')
        if person:
            self.human_x = round(person['x'] * 4, 1)

            speed = 90 if self.lidar_detect == 0 else 60 if self.lidar_detect == 1 else 30
            self.bot.forward(speed)

    def run(self):
        self.lidar_detect = self.lidar.check_distance(self.bot.steering)

        if self.lidar_detect != 3 :
            self.human_detect()
            self.colorS.x_cor

