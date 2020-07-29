#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:15:55 2020

@author: aymerick

      *args is indicating that the user can give as many argument as he wants.
      *args=Number(s) of the well(s)
"""

from Driver import CNC                                                         # Import the class CNC from Driver.py
import time               
import sys
sys.path.append("Parameters of each device")                                   # Add the file Parameters of each device to the path
import Config                                                                  # Import the parameters from Config.py


"""

The Wells class is used to control a 3D-mill instrument using G-codes. The 
following methods are the functions to move the device to specific wells depending 
of the parameters in Config.py

"""

class Wells:
    def __init__(self):
      """
      Instancation of the class Well.


      Parameters
      ----------
      None.

      Returns
      -------
      None.

      """
      self.port=Config.PortPrinter                                 # Assign the name of the port written in Config.py to self.port
      self.FirstMove=0                                             # Variable wich allow us to know if this is the first movement of the 3d-mill
      self.Coord={}                                                # Create a dictionnary
      self.cnc=CNC(self.port)                                      # Call the class CNC
      self.cnc.OpenConnection()                                    # Open the Connection with the device
      self.NbWells=0                                               # Count the number of wells 
      Wells.Wells_1(self)

    def Wells_1(self):
      """
      The Wells_1 method ask to the user if the printer is above the Wells_1.

      Parameters
      ----------
      None.

      Returns
      -------
      None.

      """      
      StartingPoint=input("Is the 3d-mill above the wells 1 [Y/N] ? ")                                        # Ask the user if the printer is ready to go 
      if StartingPoint == "Y" or StartingPoint==' Y' or StartingPoint=='y' or StartingPoint==' y':            # Check the response of the user
        self.Coord["ReadyToGo"]="YES"                                                                         # Say to the next instructions that we are ready to manipulate
      else :
          self.Coord["ReadyToGo"]="NO"                                                                        # Say to the next instructions that we are not ready to manipulate
          print("Go check 3d-millcoordinates.txt if you want to move the 3d-mill towards the wells_1")        # print the error message
          self.cnc.CloseConnection()                                                                          # Close the connection
    
    def CoordWells(self):
      """
      Calculate the relative coordinates of the wells depending of the starting point (Wells 1).
      The results will be saved in the dictionnary self.Coord.

      Parameters
      ----------
      None.

      Returns
      -------
      None.

      """        
      if self.Coord["Outrange"]=="Values within limits":                                                 # Check if the value is fine
          F=((self.TargetWells)//Config.NbWellsWidth+1)                                                  # Calculate the quotient + 1  (For example: 2/5 will give us 1)
          G=(self.TargetWells)%Config.NbWellsWidth                                                       # Calculate the rest (For example: 2/5 will give us 2)
          if G != 0 :                                                                                    # If the rest is !=0, that means we are not at the last wells of a line in Y
            self.Coord['Xwell '+str(self.NbWells)]=F*Config.DifferenceL-Config.DifferenceL               # Calculate the relative movement in X
          else :                                                                                         # If the rest is ==0, that means we are at the last wells of a line in Y
            self.Coord['Xwell '+str(self.NbWells)]=F*Config.DifferenceL-2*Config.DifferenceL             # Calculate the relative movement in X in this specific case
          if G >> 0 :                                                                                    # If the rest is >0, that means we are not at the last wells of a line in Y
            self.Coord['Ywell '+str(self.NbWells)]=Config.DifferenceW*G-Config.DifferenceW               # Calculate the relative movement in Y
          else :                                                                                         # If the rest is ==0, that means we are at the last wells of a line Y
            self.Coord['Ywell '+str(self.NbWells)]=(Config.NbWellsWidth-1)*Config.DifferenceW            # Calculate the relative movement Y in this specific case
          self.NbWells=self.NbWells+1                                                                    # Add 1 to the number of wells


    def MoveWells(self,TargetWells):
      """
      The MoveWells method move the device to TargetWell if the coordinates are within limits.
      We Move in relative coordinates

      Parameters
      ----------
      TargetWell : Number of the well

      Returns
      -------
      None.

      """      
      try:
          self.TargetWells=TargetWells                                                                          # Save the value of the TargetWells in self.TargetWells
          Wells.CheckValue(self)                                                                                # Check if the Well is within limits
          Wells.CoordWells(self)                                                                                # Caluclate the relative coordinates of the wells from Wells 1
          if self.Coord["Outrange"]=="Values within limits" and self.Coord["ReadyToGo"]=="YES" :                     # Check if the value is fine and if we are ready to manipulate
              if self.FirstMove==0:                                                                                 # If this is the first movement 
                  self.FirstMove=1                                                                                  # Change the value of FirstMove
                  self.cnc.Move(91,self.Coord['Xwell 0'] ,self.Coord['Ywell 0'],0)                                  # Move the 3d-mill to the wells in relative movement
                  self.cnc.Move(91,0,0,-2)
              else:                                                                                                 # If this is not the first movement, the relative movement will depend of the current position of the device
                  self.cnc.Move(91,0,0,2)
                  X=self.Coord['Xwell '+str(self.NbWells-1)]-self.Coord['Xwell '+str(self.NbWells-2)]               # Calculate the relative movement in X depending of the target position and the current poisiotn of the device
                  Y=self.Coord['Ywell '+str(self.NbWells-1)]-self.Coord['Ywell '+str(self.NbWells-2)]               # Calculate the relative movement in Y depending of the target position and the current poisiotn of the device
                  self.cnc.Move(91,X,Y,0)                                                                           # Move the 3d-mill to the wells in relative movement
                  self.cnc.Move(91,0,0,-2)
      except KeyError:
          pass
                
    def CheckValue(self):
      """
      The CheckValue method check if the coordinates given by the user are within limits.
      If they are not we print a message.

      Parameters
      ----------
      None.

      Returns
      -------
      None.

      """        
      try:
          if self.TargetWells<=0 or self.TargetWells>=(Config.NbWellsWidth*Config.NbWellsLength):                 # Check if the value is in the limit depending of the file Config.py
                  self.Coord["Outrange"]="Values out of the limits"                                               # If they are not we save the result in self.Coord["Outrange"]
                  print('The Wells '+str(self.TargetWells)+" is out of range. Please check Config.py")            # We print a message to the user
          else :
                    self.Coord["Outrange"]="Values within limits"                                                 # If they are in the limits we save the answer in self.Coord["Outrange"]
                  
      except TypeError:                                                                                           # In case the user has written a <str> instead of a number
              print('Please write numbers')                                                                      
              self.Coord["Outrange"]="Values out of the limits"
              
    def CloseConnection(self):
      """
      The CloseConnection method close the connection with the device and put the printer
      above the wells_1

      Parameters
      ----------
      None.

      Returns
      -------
      None.
      
      """
      try:
          if self.NbWells>>0 and self.Coord["ReadyToGo"]=="YES" :   
              self.cnc.Move(91,0,0,2)
              self.cnc.Move(91,-self.Coord['Xwell '+str(self.NbWells-1)],-self.Coord['Ywell '+str(self.NbWells-1)],0)    # Move the printer back to the Wells_1
          self.cnc.CloseConnection()                                                                                     # Close the connection with the 3d-mill
      except ValueError:
          pass
              
          
            
if __name__ == "__main__":  
    Test = Wells()       
    Test.MoveWells(7)
    time.sleep(2)
    Test.MoveWells(9)
    time.sleep(2)
    Test.CloseConnection()


