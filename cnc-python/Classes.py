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
    
    def Ouverture(self):
        try:
            self.s  = serial.Serial(self.port,115200);
            print("Port "+self.port+" ouvert")
            time.sleep(2)
            self.s.flushInput()
            cnc.Homing()
        except serial.SerialException:
            print("Le Port "+self.port+" est déja ouvert ou n'est pas branché ")
            pass
        
    def Gcode(self,X,Y,Z):
        self.s.flushInput()
        string2Send="G00 G91 X"+str(X)+" Y"+str(Y)+" Z"+str(Z)+"\n"
        print(type(string2Send))
        print("Sending :{}".format(string2Send))
        cnc.Statut()
        while self.B[0].strip("<")=="Run":
            print("on attend")
            time.sleep(2)
            cnc.Statut()
        self.s.write(string2Send.encode())
        grbl_out = self.s.readline() 
        print(" : " + grbl_out.decode().strip())
        
    def Fermeture(self):
        try:
            time.sleep(5)
            self.s.close()
            print("Port "+self.port+" fermé")
        except AttributeError:
            print("Le port "+self.port+" ne peut pas être fermé")
            
    def Test(self,X):
        f=open('TestClasses.txt','w')
        f.write("G00 G91 X"+str(X)+"\n")
        f.write("G00 G91 X"+str(X)+"\n")
        f.write("G00 G91 X"+str(X)+"\n")
        f=open('TestClasses.txt','r')
        for line in f:
            string2Send=f.readline()+"\n" #"".join([l,'\r'])  
            print("Sending :{}".format(string2Send))
            self.s.write(string2Send.encode()) # Send g-code block to grbl
            grbl_out = self.s.readline() # Wait for grbl response with carriage return
            print(" : " + grbl_out.decode().strip())
            time.sleep(5)

    def Homing(self):
        string2Send="G00 G90 X0 Y0 Z0\n"
        print(type(string2Send))
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out = self.s.readline() 
        print(" : " + grbl_out.decode().strip())
        time.sleep(5)
        
    def Statut(self):
        self.s.flushInput()
        string2Send="?"
        print("Sending :{}".format(string2Send))
        self.s.write(string2Send.encode())
        grbl_out=self.s.readline()
        A=grbl_out.decode().strip()
        caractere = "|";
        self.B=A.split(caractere)
        print("L'imprimante est : "+self.B[0].strip("<"))
        
if __name__ == "__main__":

    cnc = CNC('COM4')
    cnc.Ouverture()
    cnc.Gcode(60,0,0)
    cnc.Gcode(-60,0,0)
    cnc.Fermeture()
    
#CNC.Ouverture('COM4')
#CNC.GcodeXY(-20,-10)
#time.sleep(5)
#CNC.Fermeture('COM4')
#except SerialException :
  #print("Sending :{}".format(string2Send))
   #         self.s.write(string2Send.encode())
    #        grbl_out = self.s.readline() 
     #       print(" : " + grbl_out.decode().strip())