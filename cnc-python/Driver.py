# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:24:47 2020

@author: Aymerick Reinders

The CNC class is used to control a 3D-mill instrument using G-codes. The 
following methods are the most basic functions that are neede to interact with
the device.

"""

import time
import serial

class CNC:
    
    # For the class instanciation, the input variable port is indicating which 
    # COM port the 3D-Mill is connected to.
    # -------------------------------------
    
    def __init__(self,port):
        self.port = port   
        return
    
    # The OpenConnection method is opening the serial communication port and 
    # keeps the output in self.
    # The time delay of 2s is important to keep, else the communication will 
    # not be established and it won't be possible to control the 3D-mill.
    # When an error occurs, Python will normally stop and generate an error message.
    # We will change this message by using "try" and "except"
    # --------------------------------
    
    def OpenConnection(self):
        try:                                            # The try block lets you test a block of code for errors.
            self.s  = serial.Serial(self.port,115200);  # Open the port and keeps the output in self.s
            print("Port "+self.port+" opened")
            time.sleep(2)
            self.s.flushInput()                         # Remove data from input buffer
        except serial.SerialException:                  # The except block lets you handle the error.
            print("The port "+self.port+" is already opened or is not connected ")
            pass
        
    # The Move method is sending instructions to the 3D-mill in order to 
    # change the positions of the motors.The user must indicate the 
    # X,Y,Z coordinates as input.
    # ---------------------------
   
    def Move(self,X,Y,Z):
        self.s.flushInput()                                             # Remove data from input buffer
        string2Send="G00 G91 X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"     # Translate X,Y,Z coordinates into G-code
        print("Sending :{}".format(string2Send))                        # Write to the user what G-code is sent to the 3D-mill
        self.s.write(string2Send.encode())                              # Send g-code block to grbl (the 3D-mill)
        grbl_out = self.s.readline()                                    # Wait for grbl response with carriage return
        print(" : " + grbl_out.decode().strip())  
        
    # The Status method is checking if the 3D-mill is doing something or not
    # ------------------------------------

    def Status(self):
        self.s.flushInput()                              # Remove data from input buffer
        string2Send="?"                                  # This G-code input ask to the 3D-mill what is his state 
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()                      # The typical answer is: <Idle|MPos:0.000,0.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>
        A=grbl_out.decode().strip()                     # We just want the state so we will cut the message in 4 
        caractere = "|";                                # by using .split 
        self.B=A.split(caractere)
        print("Printer State : "+self.B[0].strip("<"))  # We print the first part of the message which is the state of the 3D-mill                

    # The WaitForIdle method wait 2 sec if the 3D-mill is already working
    # -------------------------------------------------------------------
         
    def WaitForIdle(self):
        CNC.Status(self)                                # Check the state of the device
        while self.B[0].strip("<")=="Run":              # Wait until the status is no longer "run"
            print("Wait")                               # we wait 2 sec
            time.sleep(2)
            CNC.Status(self)                            # Check if the status has changed

    # Set the starting coordinates of the 3D-mill
    # --------------------------------------
            
    def Homing(self):
        string2Send="G00 G90 X0 Y0 Z0\n"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out = self.s.readline() 
        print(" : " + grbl_out.decode().strip())
        
    # Read the machine position (Mpos - absolute position) of the 3D-mill
    # -------------------------------------------------------------------
        
    def Read_MPos(self):
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        A=grbl_out.decode().strip()
        caractere="|"
        M=A.split(caractere)
        print(M[1])                 # We print the second part of the message wich is the Mpos of the 3D-mill

    # Read the working position (Wpos - relative position) of the 3D-mill
    # -------------------------------------------------------------------
        
    def Read_WPos(self):
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        E=grbl_out.decode().strip()
        caractere="|"
        W=E.split(caractere)
        print(W[3])                   # We print the fourth part of the message wich is the Wpos of the 3D-mill
        
    # Read the FS of the 3D-mill
    # -------------------------------------   
        
    def FS(self):
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        A=grbl_out.decode().strip()
        caractere="|"
        F=A.split(caractere)
        print(F[2])                 # We print the third part of the message wich is the Wpos of the 3D-mill
        
        
    # The CloseConnection method is closing the serial communication port.
    # The time delay of 5s is important tobe sure that all the instruiction 
    # has been executed.
    # ----------------------------------
        
    def CloseConnection(self):
        try:
            time.sleep(5)
            self.s.close()
            print("Port "+self.port+" closed")
        except AttributeError:
            print("The port "+self.port+" can't be closed")
             

if __name__ == "__main__":

    cnc = CNC('COM4')
    cnc.OpenConnection()
    cnc.Homing()
    cnc.Move(5,0,0)
    cnc.WaitForIdle()
    cnc.Move(-10,0,0)
    cnc.WaitForIdle()
    cnc.MPositions()
    cnc.WPositions()
    cnc.CloseConnection()
    
#CNC.Ouverture('COM4')
#CNC.GcodeXY(-20,-10)
#time.sleep(5)
#CNC.Fermeture('COM4')
#except SerialException :
  #print("Sending :{}".format(string2Send))
   #         self.s.write(string2Send.encode())
    #        grbl_out = self.s.readline() 
     #       print(" : " + grbl_out.decode().strip())
    
#   def Test(self,X):
#        f=open('TestClasses.txt','w')
#        f.write("G00 G91 X"+str(X)+"\n")
#        f.write("G00 G91 X"+str(X)+"\n")
#        f.write("G00 G91 X"+str(X)+"\n")
#        f=open('TestClasses.txt','r')
#        for line in f:
#            string2Send=f.readline()+"\n" #"".join([l,'\r'])  
#            print("Sending :{}".format(string2Send))
#            self.s.write(string2Send.encode()) # Send g-code block to grbl
#            grbl_out = self.s.readline() # Wait for grbl response with carriage return
#            print(" : " + grbl_out.decode().strip())
#            time.sleep(5)
