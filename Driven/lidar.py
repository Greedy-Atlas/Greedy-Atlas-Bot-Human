from pop.LiDAR import Rplidar
import math
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
        for degrees, distance, _ in V :
            if degrees > 0 + sub_value and degrees < 360 - sub_value:
                continue
            else :
                if distance < self.length[2]:
                    detect = 3
                    break
                elif distance < self.length[1] :
                    detect = 2
                    break
                elif distance < self.length[0]:
                    detect = 1
                    break
        print("detect %d"%(detect))     # Debug
        return detect