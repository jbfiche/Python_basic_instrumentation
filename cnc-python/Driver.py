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
        return
    
    def OpenConnection(self):
        try:
            self.s  = serial.Serial(self.port,115200);
            print("Port "+self.port+" opened")
            time.sleep(2)
            self.s.flushInput()
        except serial.SerialException:
            print("The port "+self.port+" is already opened or is not connected ")
            pass
        
    def Moove(self,X,Y,Z):
        self.s.flushInput()
        string2Send="G00 G91 X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"
        print(type(string2Send))
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out = self.s.readline() 
        print(" : " + grbl_out.decode().strip())
        
    def WaitForIdle(self):
        CNC.Statut(self)
        while self.B[0].strip("<")=="Run":
            print("Wait")
            time.sleep(2)
            CNC.Statut(self)

    def Homing(self):
        string2Send="G00 G90 X0 Y0 Z0\n"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out = self.s.readline() 
        print(" : " + grbl_out.decode().strip())
        
    def Statut(self):
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        A=grbl_out.decode().strip()
        caractere = "|";
        self.B=A.split(caractere)
        print("Printer State : "+self.B[0].strip("<"))
        
    def MPositions(self):
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        A=grbl_out.decode().strip()
        caractere="|"
        M=A.split(caractere)
        print(M[1])

    def WPositions(self):
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        E=grbl_out.decode().strip()
        caractere="|"
        W=E.split(caractere)
        print(W[3])
   
    def FS(self):
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        A=grbl_out.decode().strip()
        caractere="|"
        F=A.split(caractere)
        print(F[2])
        
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
    cnc.Moove(5,0,0)
    cnc.WaitForIdle()
    cnc.Moove(-10,0,0)
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
