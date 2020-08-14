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
from threading import Thread

NewFile={}                              # Create a dictionnary
NumberOfNewFiles=0                      # Count the amount of new files in the depository
AlreadyProcessed=0                     # Count the amount of file already copied 
CheckFinished=False                     # Check if the class read has finished to check the folder

class Read(Thread):
    """
    
    The goal of this class is to check if there is a new file in target folder.
    If there is, we want to identify wich one et analyze it with the other class.
    We want to be able to do both Read and Analyze at the same time, so we will use thread.

    Parameters
    ----------
    None.
    
    Returns
    -------
    None.

    
    """
    
    def __init__(self):
        """
        Initialisation of the class
        
        Returns
        -------
        None.
        
        """
        Thread.__init__(self)        # Initialisation of thread
        
    def run(self): 
        """
        The run method is checking if there is any new file in target folder.
        If there is, we will copy it to target folder with the class Analyze

        Returns
        -------
        None.
        
        """
        global NewFile                                          # Call the variable defined outside the class
        global NumberOfNewFiles                                 # We want the variable to be global, because we will use it in the other class 
        global CheckFinished                                    # This is how the class will be able to interact with each other.
        
        for i in range (0,MP.Duration):                         # We want to check the file during all the manipulation. So, the user will write the duration of the manipulation in ManipulationParameters.py
            OLD=glob.glob(MP.Path2+"*.json")                    # Check what contains the folder. MP.Path2 → Path to the folder
            time.sleep(1)                                       # Wait one second
            NEW=glob.glob(MP.Path2+"*.json")                    # Check if the programms in the folder has changed. (Important: If there is new data but their format are not corresponding to MP.Format, NEW and OLD will be the same)
            if OLD != NEW:                                      # Check if something has changed during the one second delay
                if len(OLD)==0:                                 # See if it's the first time a new file (or more) is in the folder
                    for l in range (0,len(NEW)):                # We want to copy all the new files
                        NewFile[NumberOfNewFiles]=NEW[l]        # Save all the path in the dictionnary. (NEW[l] looks like this '/home/aymerick/Desktop/Directory1/Test.rst')
                        NumberOfNewFiles=NumberOfNewFiles+1     # Add one to the number of new files
                else:                                           # If it's not the first time a file is added to the folder
                    for i in range (0,len(NEW)):                
                        for k in range (0,len(OLD)):            # The position of each file may change in the folder (alphabetical order). So, we will compare each file in NEW to each file in OLD.
                            if NEW[i]==OLD[k]:                  # If the file is in OLD and in NEW, nothing happens
                                FileInTheList=True 
                                break
                            else:                               # In the case the file is only in NEW, we want to copy it 
                                FileInTheList=False
                        if FileInTheList==False:
                            NewFile[NumberOfNewFiles]=NEW[i]    # Save all the path in the dictionnary.
                            NumberOfNewFiles=NumberOfNewFiles+1 # Add one to the number of new files
        CheckFinished=True                                      # The class has finished to check the folder (The manipulation is finished)
        print("Check Finished")



class Analyze(Thread):
    """
    
    The goal of this class is to analyze new files while the user is acquiring data.
    We want to be able to do both Read and Analyze at the same time, so we will use thread.

    Parameters
    ----------
    None.
    
    Returns
    -------
    None.

    
    """
    
    def __init__(self):
        """
        Initialisation of the class
        
        Returns
        -------
        None.
        
        """
        Thread.__init__(self)        # Initialisation of thread

    def run(self):
        """
        The run method is checking if there is any new file in target folder.
        If there is, we will analyze it with the class Analyze.

        Returns
        -------
        None.
        
        """  
        global NewFile                                                           # Call the variable defined outside the class and modified (or not) by the class Read()
        global NumberOfNewFiles
        global AlreadyProcessed
        global CheckFinished

        while CheckFinished==False or AlreadyProcessed != NumberOfNewFiles:      # We want to check if a new file has been detected by Read() but when Read() has finished (manipulation is over), we want to stop checking.     
            if AlreadyProcessed != NumberOfNewFiles:                             # If Read() has detected new files
                for i in range (AlreadyProcessed,NumberOfNewFiles):              # We want to copy all of the new files
                    AlreadyProcessed=AlreadyProcessed+1                          # We analyzed one file so we add one to the value of AlreadyCopied
                    time.sleep(4)                                                # This time is to simulate a long time for the copy (you can delete it)
                    Caractere="/"
                    Prog=NewFile[i].split(Caractere)                             # We are looking for the name of the new file
                    os.chdir(MP.Path2)                                           # Change the working directory to MP.Path2 (Where we want to open the file; Directory 2 in our case)
                    File=open(str(Prog[len(Prog)-1]),"r")                        # Open the file
                    Test=json.loads(File.read())                                 # Read the file 
                    
                    print(Test)                                                  # Analyze the currrent file (in our case, we just print it)
                                      
                    File.close()                                                 # Close the file
                    
if __name__=="__main__":
    
    Thread_1=Read()
    Thread_2=Analyze()
    
    Thread_1.start()
    Thread_2.start()
    
    Thread_1.join()
    Thread_2.join()
           