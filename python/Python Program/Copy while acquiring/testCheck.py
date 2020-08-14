#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 12:55:55 2020

@author: marcnol
"""


# imports
import glob
import time
import json
import os
from threading import Thread

# global parameters
Path1="/mnt/grey/DATA/users/marcnol/test_HiM/HiM2colors/"
Format=".rst"                                                  # Format of the data
Path2="/mnt/grey/DATA/users/marcnol/test_HiM/HiM2colors/tmp/"
Duration=40                                                    # Duration of manipulation (sec)
DurationProcess=30                                             # Duration of the process

NewFile=[]                              # Create a dictionnary
NumberOfNewFiles=0                      # Count the amount of new files in the depository
AlreadyProcessed=0                     # Count the amount of file already copied 
CheckFinished=False                     # Check if the class read has finished to check the folder


# functions
def getFileList(Path,Format):
    return glob.glob(Path+"*"+Format)

# parameters
waitBeforeNewCheck=1

# preprecessing
newFile=getFileList(Path1,Format)
NumberOfNewFiles=len(newFile)
print("Original list of files: \n{}".format(newFile))
print("\n Press q-Enter to quit at any time!")

# looks for files
for i in range (0,Duration): 
    oldFileList=getFileList(Path1,Format)
    time.sleep(waitBeforeNewCheck)           
    newFileList=getFileList(Path1,Format)
    if oldFileList!= newFileList:
        listNewFiles=[x for x in newFileList if x not in oldFileList]
        NumberOfNewFiles=len(listNewFiles)
        NewFile.append(listNewFiles)
        print("New file added: \n{}".format(listNewFiles))

    val = input() 
    if val=='q':
        break
                    
CheckFinished=True               
print("Check Finished")
