#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 12:55:55 2020

@author: marcnol
"""


import glob
import time
import json
import os
from threading import Thread


Path1="/mnt/grey/DATA/users/marcnol/test_HiM/HiM2colors/"
Format=".rst"                                                  # Format of the data
Path2="/mnt/grey/DATA/users/marcnol/test_HiM/HiM2colors/tmp/"
Duration=40                                                    # Duration of manipulation (sec)
DurationProcess=30                                             # Duration of the process


NewFile=[]                              # Create a dictionnary
NumberOfNewFiles=0                      # Count the amount of new files in the depository
AlreadyProcessed=0                     # Count the amount of file already copied 
CheckFinished=False                     # Check if the class read has finished to check the folder


def getFileList(Path,Format):
    return glob.glob(Path+"*"+Format)


waitBeforeNewCheck=1

for i in range (0,Duration):                         # We want to check the file during all the manipulation. So, the user will write the duration of the manipulation in ManipulationParameters.py
    if i==0:
        newFile=getFileList(Path1,Format)
        NumberOfNewFiles=len(newFile)
        print("Original list of files: \n{}".format(newFile))
        
    oldFileList=getFileList(Path1,Format)
    time.sleep(waitBeforeNewCheck)                                       # Wait one second
    newFileList=getFileList(Path1,Format)
    if oldFileList!= newFileList:                                      # Check if something has changed during the one second delay
        listNewFiles=[x for x in newFileList if x not in oldFileList]
        NumberOfNewFiles=len(listNewFiles)
        NewFile.append(listNewFiles)
        print("New file added: \n{}".format(listNewFiles))
                    
CheckFinished=True                                      # The class has finished to check the folder (The manipulation is finished)
print("Check Finished")
