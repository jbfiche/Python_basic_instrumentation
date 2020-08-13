#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:10:38 2020

This file contains all the methods to Read and analyze files without threading 

@author: aymerick
"""

import glob
import time
import json
import os
import ManipulationParameters as MP

for i in range (0,MP.DurationProcess):        # We want to check the file during all the manipulation (and maybe more depending of the time needed for the copy). So, the user will write the duration of the manipulation in ManipulationParameters.py
    
    OLD=glob.glob(MP.Path2+"*.json")          # Check what contains the folder. MP.Path2 → Path to the folder.
    time.sleep(1)
    NEW=glob.glob(MP.Path2+"*.json")          # Check if what contains the folder has changed
    
    NewFile={}                                # Create a dictionnary 
    NumberOfNewFiles=0
    
    if OLD != NEW:
        if len(OLD)==0:
            for l in range (0,len(NEW)):
                NewFile[NumberOfNewFiles]=NEW[l]
                NumberOfNewFiles=NumberOfNewFiles+1
        else:
            for i in range (0,len(NEW)):
                for k in range (0,len(OLD)):                       # Read
                    if NEW[i]==OLD[k]:
                        FileInTheList=True 
                        break
                    else:
                        FileInTheList=False
                if FileInTheList==False:
                    NewFile[NumberOfNewFiles]=NEW[i]
                    NumberOfNewFiles=NumberOfNewFiles+1
                    
        for i in range (0,NumberOfNewFiles):
           Caractere="/"
           Prog=NewFile[i].split(Caractere)
           os.chdir(MP.Path2)
           File=open(str(Prog[len(Prog)-1]),"r")                  # Open and Process
           Test=json.loads(File.read())
           print(Test)
           File.close()
           