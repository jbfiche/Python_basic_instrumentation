# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:38:11 2020

@author: admin

The MS2000 class is used to control a translation plate using specific-codes. The 
following methods are the most basic functions that are neede to interact with
the device.

"""
import time
import serial

class MS2000:
    
    def __init__(self,port):
        """
        For the class instanciation, the input variable port is indicating which 
        COM port the 3D-Mill is connected to.

        Parameters
        ----------
        port : Name of the port where the printer is connected (COM4 in our case)

        Returns
        -------
        None.

        """
        self.port=port                    # Save the name of the port into the variable "self.port"
        self.MSState={}                   # Create a dictionnary
        self.ROI=open("ROI.txt","a")      # Open the file "ROI.txt" in append mode.The program adds the text to the end of the file. 
        self.GoTo=open("ROI.txt","r")     # Open the file "ROI.txt" in read mode.The program reads the text and save it into "self.GoTo"
        
    def OpenConnection(self):
        """
        The OpenConnection method is opening the serial communication port and 
        keeps the output in self.s
        When an error occurs, Python will normally stop and generate an error message.
        We will change this message by using "try" and "except"

        Returns
        -------
        None.

        """
        
        try:                                                                                                # The try block lets you test a block of code for errors.                                        
            self.s=serial.Serial(self.port,9600,serial.EIGHTBITS,serial.PARITY_NONE,serial.STOPBITS_ONE);   # Open the port and keeps the output in self.s
            self.s.flushInput()                                                                             # Remove data from input buffer                     
        except serial.SerialException:                                                                      # The except block lets you handle the error.         
            print("The port "+self.port+" is already opened or is not connected ")
            
            
    def Status(self):
        """
        The Status method is checking if the MS2000 is doing something or not

        Returns
        -------
        None.

        """
        self.s.flushInput()                      # Remove data from input buffer
        string2Send="/ \r"                       # This str input ask to the MS2000 what is his state (Command : STATUS)                 
        self.s.write(string2Send.encode())       # Send the input to the MS2000 encoded in UTF-8
        Output=self.s.readline()                 # Read the output
        self.MSState["State"]=Output.decode()    # Save the response in the dictionnary (B = Still working;N = Move finished)
            
    def WaitForIdle(self):
        """
        The WaitForIdle method wait 1 sec if the MS2000 is already working

        Returns
        -------
        None.

        """
        MS2000.Status(self)                            # Check the state of the device
        Waiting_time=0
        while self.MSState["State"]!="N\r\n":          # Wait until the state is "N" (Move finished)
            time.sleep(1)                              # We wait 1sec
            Waiting_time=Waiting_time+1
            MS2000.Status(self)                        # Check if the status has changed
            if Waiting_time>=15:                       # If we wait to much there might be an error
                print("Temps limite dépassé")          # Print an error message
                break                                  # Stop the method
            
            
            
    def MoveREL(self,X,Y):
        """
        The MoveREL method is sending instructions to the MS2000 in order to 
        change the positions of the motors.The user must indicate the 
        X,Y coordinates as input. This method uses relative movements depending of
        the last coordinates of the device.
        We multiply the X and Y coordinates by 10 because we want them in tenths of 
        microns and the user will write them in microns (easier to use)

        Parameters
        ----------
        X : X coordinates
        Y : Y coordinates

        Returns
        -------
        None.
        
        """
        self.s.flushInput()                                   # Remove data from input buffer
        string2Send="R X="+str(X*10)+" Y="+str(Y*10)+"\r"     # This str input ask to the device to move by using relative movements. (Command : MOVREL)
        self.s.write(string2Send.encode())                    # Send the input to the MS2000 encoded in UTF-8
        MS2000.WaitForIdle(self)                              # Wait until the device has finished his movement by using the WaitForIdle() method
        
        
    def MoveABSOL(self,X,Y):
        """
        The MoveABSOL method is sending instructions to the MS2000 in order to 
        change the positions of the motors.The user must indicate the 
        X,Y coordinates as input. This method uses absolute movements. Pay attention,
        the coordinates may change if the home (0,0) position changes.
        We multiply the X and Y coordinates by 10 because we want them in tenths of 
        microns and the user will write them in microns (easier to use)

        Parameters
        ----------
        X : X coordinates
        Y : Y coordinates

        Returns
        -------
        None.
        
        """        
        self.s.flushInput()                                  # Remove data from input buffer
        string2Send="M X="+str(X*10)+" Y="+str(Y*10)+"\r"    # This str input ask to the device to move by using absolute movement (Command : MOVE)
        self.s.write(string2Send.encode())                   # Send the input to the MS2000 encoded in UTF-8
        MS2000.WaitForIdle(self)                             # Wait until the device has finished his movement by using the WaitForIdle method
        
    def AxisPosition(self):
        """
        The AxisPosition method ask to the device his coordinates (X,Y).
        No matter in wich order the X,Y and Z's are specified in the WHERE
        command, the reply will always be in the order X,Y,Z

        Returns
        -------
        None.

        """
        self.s.flushInput()                     # Remove data from input buffer
        string2Send="W X Y\r"                   # This str input ask to the device his current position for the axis specified (Command : WHERE)
        self.s.write(string2Send.encode())      # Send the input to the MS2000 encoded in UTF-8
        self.Output=self.s.readline()           # Read the output and save it in "self.Output". The coordinates are absolute
      
    def MemorizeROI(self):
        """
        The MemorizeROI method save the coordinates of an ROI (Range Of Interest)
        in the file "ROI.txt".

        Returns
        -------
        None.

        """
        MS2000.AxisPosition(self)                                                   # Ask the coordinates of the device by using the AxisPosition method 
        Coordinates=self.Output.decode()                                            # Translate the response in str (previously in UTF-8) and save it into Coordinates. Typical response ":A 12345 6213"
        caractere=" "                                                               # We only want X,Y coordinates so we will split the response
        Split=Coordinates.split(caractere)                                          # Split coordinates into a list where each "word" is a list item
        X=Split[1]                                                                  # Split[0] is ":A" so X coordinates will be Split[1]
        Y=Split[2]                                                                  # The coordinates are given in tenths of microns. We want them in microns 
        X=X[0:len(X)-1]+"."+X[len(X)-1]                                             # Add a coma between the last digit and the one before (12345 → 1234,5)
        Y=Y[0:len(Y)-1]+"."+Y[len(Y)-1]                                             # The user will get the data in microns instead of tenths of microns
        self.ROI.write("ROI : "+str(X)+" "+str(Y)+"\r\r")                           # Write "ROI : X Y" in the "ROI.txt" file
        
    def GOTOROI(self):
        """
        The GOTOROI method move the device to all the coordinates of ROI (Range Of Interest)
        saved in the file "ROI.txt".

        Returns
        -------
        None.

        """
        lines=self.GoTo.readlines()                  # Save all the lines of "ROI.txt" in the variable lines
        Nboflines=len(lines)                         # Count the amount of lines
        for i in range(0,Nboflines):                 
            Currentline=lines[i]
            if Currentline[0:3]=="ROI":              # If the first 3 terms of the line are "ROI", the program will do an action otherwise it will do nothing   
                caractere=" "                        # We only want X,Y coordinates so we will split the reponse 
                Split=Currentline.split(caractere)   # Split coordinates into a list where each "word" is a list item
                X=float(Split[2])                    # X coordinates will be in Split[2]
                Y=float(Split[3])                    # Y coordinates will be in Split[3]
                MS2000.MoveABSOL(self,X,Y)           # Move the MS2000 to the ROI
                
    def Speed(self,X,Y):
        """
        The Speed method sets the maximum speed at wich the stage will move.
        Speed set in millimeters per second. Maximum speed is 7.5 mm/s for 
        standard 6.5 mm pitch leadscrews.

        Returns
        -------
        None.

        """
        self.s.flushInput()                           # Remove data from input buffer
        string2Send="S X="+str(X)+" Y="+str(Y)+"\r"   # This str input change the movement speed of the device
        self.s.write(string2Send.encode())            # Send the input to the MS2000 encoded in UTF-8
                
    def CloseConnection(self):
        """
        The CloseConnection method is closing the serial communication port.
        The time delay of 2s is important to be sure that all the instruiction 
        has been executed.

        Returns
        -------
        None.

        """
        time.sleep(2)          # Wait 2sec
        self.s.close()         # Close the communication with the serial port
        self.ROI.close()       # Close the file "ROI.txt" opened in append mode 
        self.GoTo.close()      # Close the file "ROI.txt" opened in read mode 
        
if __name__ == "__main__":
    MS=MS2000('COM4')
    MS.OpenConnection()
    MS.MemorizeROI()
    # MS.GOTOROI()
    MS.CloseConnection()
    