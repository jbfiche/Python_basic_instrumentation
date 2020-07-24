# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:37:33 2020

@author: NoelFlantier
"""


# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:24:47 2020

@author: Aymerick Reinders

The CNC class is used to control a 3D-mill instrument using G-codes. The 
following methods are the most basic functions that are neede to interact with
the device.


"""

MotorLimit={}
MotorLimit["XhighMM"]=295.0
MotorLimit["YhighMM"]=145.0
MotorLimit["ZhighMM"]=45.0
MotorLimit["Absolute"]=90
MotorLimit["Relative"]=91

import time
import serial
import Config

class CNC:
    
    def __init__(self,port):
        """
        For the class instanciation, the input variable port is indicating which 
        COM port the 3D-Mill is connected to.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        self.port=port
        self.log_file=open("log_file.txt","w")
        self.PrinterState={}
        return

    def OpenConnection(self):
        """
        The OpenConnection method is opening the serial communication port and 
        keeps the output in self.
        The time delay of 2s is important to keep, else the communication will 
        not be established and it won't be possible to control the 3D-mill.
        When an error occurs, Python will normally stop and generate an error message.
        We will change this message by using "try" and "except"

        Returns
        -------
        None.

        """
        try:                                            # The try block lets you test a block of code for errors.
            self.s  = serial.Serial(self.port,115200);  # Open the port and keeps the output in self.s
            self.log_file.write("Port "+self.port+" opened\n")
            time.sleep(2)
            self.s.flushInput()                         # Remove data from input buffer
        except serial.SerialException:                  # The except block lets you handle the error.
            print("The port "+self.port+" is already opened or is not connected ")
            self.log_file.write("The port "+self.port+" is already opened or is not connected ")
            self.log_file.close()                       #To be sure the message is written
            pass

    def Homing(self):
        """
        Set the starting coordinates of the 3D-mill

        Returns
        -------
        None.

        """
        string2Send="G90 X0 Y0 Z0\n"
        self.log_file.write("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out = self.s.readline() 
        self.log_file.write(" : " + grbl_out.decode().strip()+"\n")  
        CNC.WaitForIdle(self)
        

    def Status(self):
        """
        The Status method is checking if the 3D-mill is doing something or not

        Returns
        -------
        None.

        """
        self.s.flushInput()                              # Remove data from input buffer
        string2Send="?"                                  # This G-code input ask to the 3D-mill what is his state 
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()                      # The typical answer is: <Idle|MPos:0.000,0.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>
        A=grbl_out.decode().strip()                     # We just want the state so we will cut the message in 4 
        caractere = "|";                                # by using .split 
        B=A.split(caractere)
        self.PrinterState["State"]=B[0]
        self.PrinterState["MPos"]=B[1]
        self.PrinterState["FS"]=B[2]
        self.PrinterState["WPos"]=B[1]
         
    def WaitForIdle(self):
        """
        The WaitForIdle method wait 0.1 sec if the 3D-mill is already working

        Returns
        -------
        None.

        """
        CNC.Status(self)                                                 # Check the state of the device
        WaitingTime=0                              
        while self.PrinterState["State"].strip("<")=="Run":              # Wait until the status is no longer "run"
            time.sleep(0.1)                                              # we wait 100 msec
            CNC.Status(self)                                             # Check if the status has changed
            WaitingTime=WaitingTime+0.1
            if WaitingTime >= 15.0:
                print("There is an error")
                self.log_file.write("There is an error, Timeout \n")
                break
            
                      
    def Move(self,G,X,Y,Z):
        """
     The Move method is sending instructions to the 3D-mill in order to 
     change the positions of the motors.The user must indicate the 
     X,Y,Z coordinates as input.

        Parameters
        ----------
        G : 90 : Absolute coordinates 91 : Relative coordinates
        X : X coordinates
        Y : Y coordinates
        Z : Z coordinates

        Returns
        -------
        G : 90 : Absolute coordinates 91 : Relative coordinates
        X : X coordinates
        Y : Y coordinates
        Z : Z coordinates

        """
        if G != 90 and G!=91:
            print("Wrong value for G. Muste be 90 or 91")
            self.log_file.write("Wrong value for G. Muste be 90 or 91\n")
        if G==90 :    
#            if 0.0<=X<=295.0 and 0.0<=Y<=145.0 and 0.0<=Z<=45.0:
                self.s.flushInput()                                                         # Remove data from input buffer
                string2Send="G00 G"+str(G)+" X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"         # Translate X,Y,Z coordinates into G-code
                self.log_file.write("Sending :{}".format(string2Send))                      # Write to the user what G-code is sent to the 3D-mill
                self.s.write(string2Send.encode())                                          # Send g-code block to grbl (the 3D-mill)
                grbl_out = self.s.readline()                                                # Wait for grbl response with carriage return
                self.log_file.write(" : " + grbl_out.decode().strip()+"\n")
                CNC.WaitForIdle(self)
                return G,X,Y,Z
#            else :
#                print("Error in the coordinates entered")
#                string2Send="G00 G"+str(G)+" X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"     
#                self.log_file.write("Sending :{}".format(string2Send))
#                self.log_file.write(" : error in the coordinates entered\n")
                
        if G==91:
#            CNC.Status(self)
#            A=self.PrinterState["MPos"].strip("MPos:")                                  # Check the absolute cooridinates of the printer
#            caractere=","
#            B=A.split(caractere)
#            X1=float(B[0])+float(X)
#            Y1=float(B[1])+float(Y)
#            Z1=float(B[2])+float(Z)
#            if X1<0.0 or Y1<0.0 or Z1<0.0:
#                string2Send="G00 G"+str(G)+" X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"     
#                self.log_file.write("Sending :{}".format(string2Send))
#                self.log_file.write(" : error in the coordinates entered X:"+str(X1)+" Y:"+str(Y1)+" Z:"+str(Z1)+"\n")
#                print("Error in the coordinates entered")
#            elif X1>295.0 or Y1>145.0 or Z1>45.0:
#                string2Send="G00 G"+str(G)+" X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"     
#                self.log_file.write("Sending :{}".format(string2Send))
#                self.log_file.write(" : Error in the coordinates enteredX:"+str(X1)+" Y:"+str(Y1)+" Z:"+str(Z1)+"\n")
#                print("error in the coordinates entered")
#            else:
                self.s.flushInput()                                                      # Remove data from input buffer
                string2Send="G00 G"+str(G)+" X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"      # Translate X,Y,Z coordinates into G-code
                self.log_file.write("Sending :{}".format(string2Send))                   # Write to the user what G-code is sent to the 3D-mill
                self.s.write(string2Send.encode())                                       # Send g-code block to grbl (the 3D-mill)
                grbl_out = self.s.readline()                                             # Wait for grbl response with carriage return
                self.log_file.write(" : " + grbl_out.decode().strip()+"\n")
                CNC.WaitForIdle(self)
                return G,X,Y,Z
                                
                
    def Read_MPos(self):
        """
        Read the machine position (Mpos - absolute position) of the 3D-mill

        Returns
        -------
        None.

        """
        self.s.flushInput()
        CNC.Status(self)
        print(self.PrinterState["MPos"])       

        
    def Read_WPos(self):
        """
        Read the working position (Wpos - relative position) of the 3D-mill

        Returns
        -------
        None.

        """
        self.s.flushInput()
        CNC.Status(self)
        print(self.PrinterState["WPos"])                  
        
        
    def FS(self):
        """
        Read the FS of the 3D-mill

        Returns
        -------
        None.

        """
        self.s.flushInput()
        CNC.Status(self)
        print(self.PrinterState["FS"])                 
  
        
    def CloseConnection(self):
        """
        The CloseConnection method is closing the serial communication port.
        The time delay of 5s is important tobe sure that all the instruiction 
        has been executed.

        Returns
        -------
        None.

        """
        try:
            time.sleep(2)
            self.log_file.write("Port "+self.port+" closed")
            self.log_file.close()
            self.s.close()
        except AttributeError:
            print("The port "+self.port+" can't be closed")
            self.log_file.write("The port "+self.port+" can't be closed")
            self.log_file.close()
             

if __name__ == "__main__":

    cnc = CNC(Config.PortPrinter)
    cnc.OpenConnection()
    cnc.Move(91,1,1,0)
    cnc.Move(91,-1,-1,0)
    cnc.CloseConnection()
    


















