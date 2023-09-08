import cv2
import numpy as np
from threading import Thread


class ColorSeperate():
  def __init__(self, cam):
    if cam==None:
      raise TypeError("It doesn't camera Type!")
    self.x_cor = 0.0
    self.y_cor = 0.0
    self.cam = cam
    self.width = cam.width
    self.height = cam.height

    self.t = Thread(target=self.run, daemon=True)
    self.t.start()

  def __trans_cor(self, percent):
    if(percent >= 50) :
      cor = -1 * (-1 * ((50+(percent-100))/50))
    elif(percent < 50) :
      cor = -1 * ((50-percent)/50)
    else:
      cor = None
    return cor

  @property
  def cor(self):
    return (self.x_cor, self.y_cor)

  def run(self):
    # Running part
    while True :
      frame = self.cam.value
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      lvalue = np.array([33, 96, 156])    # cone : [42, 103, 40]
      rvalue = np.array([61, 255, 255])    # cone : [61, 255, 255]

      mask_green = cv2.inRange(hsv, lvalue, rvalue)
      kernel = np.ones((7,7),np.uint8)

      mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
      mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

      seg_cone = cv2.bitwise_and(hsv, hsv, mask=mask_green)
      contours, hier = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      output = cv2.drawContours(seg_cone, contours, -1, (0,0,255), 3)

      # Calc Moments
      avr_arr_cX = []
      avr_arr_cY = []

      output_dst = output.copy()
      gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
      ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

      contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

      for i in contours:
        M = cv2.moments(i)
        if(M['m00'] == 0): continue
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])

        if(cX >= self.width/2-1 and cX <=self.width/2+1 and cY >= self.height/2-1 and cY <= self.height/2+1): continue
        cv2.circle(output_dst, (cX, cY), 3, (255, 100, 0), -1)
        avr_arr_cX.append(cX)
        avr_arr_cY.append(cY)
        cv2.circle(output_dst, (cX, cY), 3, (255, 100, 0), -1)

      self.x_cor = self.__trans_cor((np.mean(avr_arr_cX)/self.width)*100)
      self.y_cor = self.__trans_cor((np.mean(avr_arr_cY)/self.height)*100)