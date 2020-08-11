"""
"""
# import ctypes
import time
# import platform
# import os
# import numpy as np
# import collections
# import threading
# import contextlib
# from ctypes import c_int, c_float, c_long, c_ulong, POINTER,c_char_p
from pipython import GCSDevice
import site
site.addsitedir('C:\\Users\\NoelFlantier\\Desktop\\Stage\\Stage_Aymerick\\python\Python Program')  # Add a directory to sys.path and process its .pth files.
import Config

class MotorController:
    def __init__(self):
        self.Device="PI "+Config.PYName+" Mercury-Step SN "+Config.PYID
        self.State={}
        self.pidevice=GCSDevice()
    def OpenConnection(self):
        self.pidevice.ConnectUSB(self.Device)
        for i in range (1,Config.NbofAxes):
            MotorController.SVO(self,i,True)
            MotorController.FRF(self)
        time.sleep(10)
    def CloseConnection(self):
       self.pidevice.CloseConnection()
    def Move(self,Axes,N):
        self.Axes=Axes
        self.pidevice.MOV(self.Axes,N)
        MotorController.WaitForIdle(self)
    def SVO(self,Axes,N):
        self.pidevice.SVO(Axes,N)
    def Position(self,Axes):
        self.State["Coord"]=self.pidevice.qPOS(self.Axes)
    def SVOState(self):
        self.qSVO=self.pidevice.qSVO()
    def FRF(self):
        self.pidevice.FRF()
    def TargetMov(self):
        self.State["Target"]=self.pidevice.qPOS()
    def WaitForIdle(self):
       for i in range (0,20):
           MotorController.Position(self,self.Axes)
           A=self.State["Coord"]
           time.sleep(1)
           MotorController.Position(self,self.Axes)
           B=self.State["Coord"]
           if A==B:
               break

        
Test=MotorController()
Test.OpenConnection()
Test.Move("1",5.12266)
Test.Move("1",8.3)
Test.CloseConnection()
        

        