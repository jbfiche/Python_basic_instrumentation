#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:21:53 2020

@author: aymerick
encoding='ascii' ?
"""

import serial
import time
import Config

class Valve:
    def __init__(self):
        self.port=Config.PortValve
        self.ValveState={}
        self.ValveState["ValvePosition"]=1
        self.ValveState["Outrange"]="Values within limits"
        Valve.OpenConnection(self)
        self.NbValve=0
        
    def OpenConnection(self):
        self.s = serial.Serial(self.port,baudrate=9600,bytesize=serial.SEVENBITS,parity=serial.PARITY_ODD,stopbits=serial.STOPBITS_ONE);
        time.sleep(2)
        self.s.flushInput()
        Init="1a\r"
        self.s.write(Init.encode())
        time.sleep(0.1)
        string2Send="aLXR\r"
        self.s.write(string2Send.encode())
        Valve.WaitForIdle(self)
    
    def Status(self):
        self.s.flushInput()
        status="aF\r"
        self.s.write(status.encode())
        Line=self.s.read()
        grbl_out=self.s.read()
        self.ValveState["State"]=grbl_out.decode()
     
    def WaitForIdle(self):
        Valve.Status(self)
        WaitingTime=0
        while self.ValveState["State"]!="Y":
            print(self.ValveState["State"])
            time.sleep(1)
            Valve.Status(self)
            WaitingTime=WaitingTime+1
            if WaitingTime >= 15.0:
                print("There is an error")

    def ValveRotation(self,MD,pp):    #MD=module adress
        if 0>=pp or pp>=9:
            self.ValveState["Outrange"]="Valve number is out of the limits"
            print("Wrong Value")
#        elif MD!="a" and "b" and "c":
#            self.ValveState["Outrange"]="Valve module adress is wrong"
#            print("Wrong Address")
        else :
            if 1<=self.ValveState["ValvePosition"]<=4:
                opposite=self.ValveState["ValvePosition"]+4
            else:
                opposite=self.ValveState["ValvePosition"]-4
            if (pp-opposite)<=0:
                self.ValveState[self.NbValve]=str(MD)+"LP0"+str(pp)+"R\r"
                self.s.write(self.ValveState[self.NbValve].encode())
                self.ValveState["ValvePosition"]=pp
                self.NbValve=self.NbValve+1
                Valve.WaitForIdle(self)
            else:
                self.ValveState[self.NbValve]=str(MD)+"LP1"+str(pp)+"R\r"
                self.ValveState["ValvePosition"]=pp
                self.s.write(self.ValveState[self.NbValve].encode())
                self.NbValve=self.NbValve+1
                Valve.WaitForIdle(self) 
                
    def ExecuteMovement(self):
        if self.ValveState["Outrange"]=="Values within limits":
            for i in range (0,self.NbValve):
                self.s.write(self.ValveState[i].encode())
                Valve.WaitForIdle(self)


if __name__ == "__main__":
    a=Valve()
    a.ValveRotation("a",5)
    a.ValveRotation("a",2)
    a.ValveRotation("a",6)

