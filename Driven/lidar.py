from pop.LiDAR import Rplidar
from pop.Pilot import SerBot
import math
import numpy as np
import time

class Lidar:

    def __init__(self, length) :        # Turn On LiDAR 
        self.lidar = Rplidar()
        self.lidar.connect()
        self.lidar.startMotor()
        self.length = length
        print("Lidar Setup Complete")

    def __del__(self):                  # Turn Off LiDAR
        self.lidar.stopMotor()

    def __trans_steer(self, steering):
        return 90 * steering

    def check_distance(self, steering):
        detect = 0
        V = self.lidar.getVectors()
        sub_value = self.__trans_steer(steering)

        degrees = V[:, 0]   # Extract degrees Column
        distance = V[:, 1]  # Extract distance Column

        valid_degrees = np.logical_and(degrees > 0 + sub_value and degrees < 360 - sub_value)

        if np.any(valid_degrees):
            min_distance = np.min(distance[valid_degrees])

            if min_distance < self.length[2]:
                detect = 3
            elif min_distance < self.length[1] :
                detect = 2
            elif min_distance < self.length[0]:
                detect = 1
        print("detect %d"%(detect))     # Debug
        return detect
    
if __name__ == '__main__':
    length = [800, 400, 200]
    lidar = Lidar(length)
    bot = SerBot()
    print('[Serbot] : Lidar Loaded')

    time.sleep(3)

    for i in range(1,10):
        print(lidar.check_distance(bot.steering))
        time.sleep(1)
    
    del lidar