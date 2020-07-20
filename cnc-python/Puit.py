#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:15:55 2020

@author: aymerick
"""

from Driver import CNC    #Import the class CNC from Driver.py
import time               
import Config             #Import the parameters from Config.py

"""
The Well class is used to move the primter to specific coordinates depending of the wells choosen by the user.
"""

class Wells(CNC):
    def __init__(self):
#        """
#        Instancation of the class Well.
#        *args is indicating that the user can give as many argument as he wants
#        *args=Number(s) of the well(s)
#
#        """
      self.port=Config.PortPrinter         #Assign the name of the port written in Config.py to self.port
      self.FirstMove=0
      self.NbofMovements=0
      self.NbWells=1
      self.Coord={}
      self.Coord["Outrange"]="Values within limits"
      self.cnc=CNC(self.port)                                      #Call the class CNC
      self.cnc.OpenConnection()
      Wells.Wells_1(self)
      

    def Wells_1(self):
#        if self.limits=="Values within limits" :
          print('Connection ouverte')
#          self.cnc.Homing()
#          self.cnc.Move(90,0,0,Config.ZWell_1)              
#          self.cnc.Move(90,Config.XWell_1,Config.YWell_1,Config.ZWell_1)
#        else :
#          print('Initialization already done')

      
    def CoordWells(self):
#        """
#        Renseigner valeurs dans le fichier config
#        """
        if self.Coord["Outrange"]!="Values out of the limits":
            F=((self.Coord[self.NbWells-1])//Config.NbWellsWidth+1)
            G=(self.Coord[self.NbWells-1])%Config.NbWellsWidth
            if G != 0 :
                self.Coord['Xwell '+str(self.NbWells-1)]=F*Config.DifferenceL-Config.DifferenceL
            else :
                self.Coord['Xwell '+str(self.NbWells-1)]=F*Config.DifferenceL-2*Config.DifferenceL
            if G >> 0 :
                self.Coord['Ywell '+str(self.NbWells-1)]=Config.DifferenceW*G-Config.DifferenceW
            else :
                self.Coord['Ywell '+str(self.NbWells-1)]=(Config.NbWellsWidth-1)*Config.DifferenceW


    def MoveWells(self,TargetWell):
        try:
                self.Coord[self.NbofMovements]=TargetWell
                Wells.CheckValue(self)
                Wells.CoordWells(self)
                if self.FirstMove==0:
                    self.Coord["X"+str(self.NbofMovements)]=self.Coord['Xwell 0']
                    self.Coord["Y"+str(self.NbofMovements)]=self.Coord['Ywell 0']
                    self.FirstMove=1
                    self.NbofMovements=+1
                    self.NbWells= self.NbWells+1
                    print(self.Coord["X"+str(self.NbofMovements)])
                    print(self.Coord["Y"+str(self.NbofMovements)])
                else:
                    X=self.Coord['Xwell '+str(self.NbofMovements)]-self.Coord['Xwell '+str(self.NbofMovements-1)]
                    Y=self.Coord['Ywell '+str(self.NbofMovements)]-self.Coord['Ywell '+str(self.NbofMovements-1)]
                    self.Coord["X"+str(self.NbofMovements)]=X
                    self.Coord["Y"+str(self.NbofMovements)]=Y
                    print(self.Coord["X"+str(self.NbofMovements)])
                    print(self.Coord["Y"+str(self.NbofMovements)])
                    self.NbofMovements=self.NbofMovements+1
                    self.NbWells= self.NbWells+1
        except KeyError:
            print('')            
                
    def CheckValue(self):
      for k in range (0,self.NbWells):        #For every value in the list we check if it's ok
          try:
              if self.Coord[k]<=0 or self.Coord[k]>=(Config.NbWellsWidth*Config.NbWellsLength):  #Check if the value is in the limit
                  self.Coord["Outrange"]="Values out of the limits"
                  print('The Wells '+str(self.Coord[k])+" is out of range. Please check Config.py")
                  break
          except TypeError:                                                 #In case the user has written a <str> 
              print('Please write numbers')                         #instead of a number 
              self.Coord["Outrange"]="Values out of the limits"
              break
          
    def ExecuteMovement(self):
        if self.Coord["Outrange"]=="Values within limits":
            for i in range (0,self.NbofMovements):
#                self.cnc.Move(91,self.Coord["X"+str(i)],self.Coord["Y"+str(i)],0)
                print(self.Coord["X"+str(i)])
                print(self.Coord["Y"+str(i)])
#            self.cnc.Move(90,Config.XWell_1,Config.YWell_1,Config.ZWell_1)
#            self.cnc.Homing()


            
if __name__ == "__main__":  
    Test = Wells()       
    Test.MoveWells(18)
    Test.MoveWells(10)
    Test.MoveWells(2)
    Test.MoveWells(28)
    Test.MoveWells(68)

