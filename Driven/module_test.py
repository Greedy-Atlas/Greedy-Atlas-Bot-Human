from color_seperate import ColorSeperate
from pop.Pilot import Object_Follow, Camera, SerBot
import time
import cv2

cam = Camera(320,320)
of = Object_Follow(cam)
bot = SerBot()
bot.setSpeed(50)
of.load_model()
print('===================\n load Complete! \n')
time.sleep(3)

color = ColorSeperate(cam)

try:
    while True:
        person = of.detect(index='person')
        if person and color.x_cor:
            if person['x'] >= color.x_cor - 0.05 and person['x'] <= color.x_cor + 0.05 :
                x = round(person['x'] * 4, 1)
            else:
                x = round(color.x_cor*4, 1)
            bot.steering = 1.0 if x > 1.0 else -1.0 if x < -1.0 else x
            bot.forward()
        else:
            bot.stop()
        

except KeyboardInterrupt:
    pass
