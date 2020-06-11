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

X va de 0 à 295
Y va de 0 à 145
Z va de 0 à 45

"""

Dictionnaire={}
Dictionnaire["Xlimit"]="X value must be between 0 and 295 mm"
Dictionnaire["Ylimit"]="Y value must be between 0 and 145 mm"
Dictionnaire["Zlimit"]="Z value must be between 0 and 45 mm"

import time
import serial

class CNC:
    
    def __init__(self,port):
        """
        For the class instanciation, the input variable port is indicating which 
        COM port the 3D-Mill is connected to.

        Parameters
        ----------
        port : Name of the port where the printer is connected

        Returns
        -------
        None.

        """
        self.port = port  
        self.historique=open("historique.txt","w")
        self.Dico={}
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
            self.historique.write("Port "+self.port+" ouvert\n")
            time.sleep(2)
            self.s.flushInput()                         # Remove data from input buffer
        except serial.SerialException:                  # The except block lets you handle the error.
            print("The port "+self.port+" is already opened or is not connected ")
            self.historique.write("The port "+self.port+" is already opened or is not connected ")
            pass

    def Homing(self):
        """
        Set the starting coordinates of the 3D-mill

        Returns
        -------
        None.

        """
        string2Send="G90 X0 Y0 Z0\n"
        self.historique.write("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out = self.s.readline() 
        self.historique.write(" : " + grbl_out.decode().strip()+"\n")    
        

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
        self.B=A.split(caractere)
        # print("Printer State : "+self.B[0].strip("<"))  # We print the first part of the message which is the state of the 3D-mill                

         
    def WaitForIdle(self):
        """
        The WaitForIdle method wait 2 sec if the 3D-mill is already working

        Returns
        -------
        None.

        """
        CNC.Status(self)                                # Check the state of the device
        WaitingTime=0                              
        while self.B[0].strip("<")=="Run":              # Wait until the status is no longer "run"
            time.sleep(0.1)                             # we wait 100 msec
            CNC.Status(self)                            # Check if the status has changed
            WaitingTime=WaitingTime+0.1
            if WaitingTime >= 10.0:
                print("There is an error")
                self.historique.write("There is an error \n")
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
            self.historique.write("Wrong value for G. Muste be 90 or 91\n")
        if 0<=X<=295 and 0<=Y<=145 and 0<=Z<=45:
            self.s.flushInput()                                             # Remove data from input buffer
            string2Send="G00 G"+str(G)+" X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"     # Translate X,Y,Z coordinates into G-code
            self.historique.write("Sending :{}".format(string2Send))                        # Write to the user what G-code is sent to the 3D-mill
            self.s.write(string2Send.encode())                              # Send g-code block to grbl (the 3D-mill)
            grbl_out = self.s.readline()                                    # Wait for grbl response with carriage return
            self.historique.write(" : " + grbl_out.decode().strip()+"\n")
            return G,X,Y,Z
        else :
            print("error in the coordinates entered")
            string2Send="G00 G"+str(G)+" X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"     
            self.historique.write("Sending :{}".format(string2Send))
            self.historique.write(" : error in the coordinates entered\n")
        
    def Read_MPos(self):
        """
        Read the machine position (Mpos - absolute position) of the 3D-mill

        Returns
        -------
        None.

        """
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        A=grbl_out.decode().strip()
        caractere="|"
        M=A.split(caractere)
        print(M[1])                 # We print the second part of the message wich is the Mpos of the 3D-mill

        
    def Read_WPos(self):
        """
        Read the working position (Wpos - relative position) of the 3D-mill

        Returns
        -------
        None.

        """
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        E=grbl_out.decode().strip()
        caractere="|"
        W=E.split(caractere)
        print(W[3])                  # We print the fourth part of the message wich is the Wpos of the 3D-mill
        
        
    def FS(self):
        """
        Read the FS of the 3D-mill

        Returns
        -------
        None.

        """
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        A=grbl_out.decode().strip()
        caractere="|"
        F=A.split(caractere)
        print(F[2])                 # We print the third part of the message wich is the Wpos of the 3D-mill
  
        
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
            self.historique.write("Port "+self.port+" closed")
            self.historique.close()
            self.s.close()
        except AttributeError:
            print("The port "+self.port+" can't be closed")
            self.historique.write("The port "+self.port+" can't be closed")
            self.historique.close()
             

if __name__ == "__main__":

    cnc = CNC('COM4')
    cnc.OpenConnection()
    cnc.Homing()
    cnc.Move(91,18,5,3)
    cnc.WaitForIdle()
    cnc.Read_MPos()
    cnc.Move(91,-18,5,3)
    cnc.WaitForIdle()
    cnc.Read_MPos()
    cnc.Homing()
    cnc.WaitForIdle()
    print(Dictionnaire["Xlimit"])
    cnc.CloseConnection()
    


















