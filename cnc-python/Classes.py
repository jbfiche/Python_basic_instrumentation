# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:24:47 2020

@author: NoelFlantier
"""

import time
import serial

class CNC:
    def __init__(self,port):
        self.port = port
        
    def Ouverture(self):
        self.s  = serial.Serial(self.port,115200);
        print("Port "+port+" ouvert")

    def GcodeXY(X,Y):
        CNC.ouverture.flushInput()
        CNC.gcodeXY='G00 G91 G17 X'+str(X)+" Y"+str(Y)+'\r\n'
        print("Sending :{}".format(CNC.gcodeXY))
        CNC.ouverture.write(CNC.gcodeXY.encode())
        grbl_out = CNC.ouverture.readline() 
        print(" : " + grbl_out.decode().strip())

    def Fermeture(self):
        self.s.close()
        print("Port "+port+" fermé")
        
     

 cnc = CNC('COM4')
 cnc.Ouverture
 cnc.Fermeture

#CNC.Ouverture('COM4')
#CNC.GcodeXY(-20,-10)
#time.sleep(5)
#CNC.Fermeture('COM4')

 