"""
The PITranslationStage class is used to control a Mercury stepper motor con,troller. 
The following methods are the most basic functions that are neede to interact with
the device.

"""
import time
import pipython
import site
site.addsitedir('/home/aymerick/Desktop/Stage_Aymerick/python/Python Program')  # Add a directory to sys.path and process its .pth files.
import Config

class PITranslationStage:
    def __init__(self):
        """
        Class instanciation. We check the characteristics of the device in the 
        file config.py

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """      
        self.State={}                                                              # Create a dictionnary 
        self.pidevice=pipython.GCSDevice()                                         # Change GCSDevice() to self.pidevice
        
    def OpenConnectionUSB(self):
        """
        The OpenConnectionUSB method is opening the serial communication port 
        The OpenConnectionUSB method will also turn on the servo and do a reference 
        move for each device

        Returns
        -------
        None.

        """
        try:
            for i in range (1,Config.NbofAxes+1):                                           # We initialize each device   
                self.Device="PI "+Config.PYName[i-1]+" Mercury-Step SN "+Config.PYID[i-1]   # Save the full name of the device
                self.pidevice.ConnectUSB(self.Device)                                       # Open the connection with the current device
                self.pidevice.SVO(str(i),True)                                              # Set servo control for the current axes on "on"
                self.pidevice.FNL(str(i))                                                   # Start a reference move to the negative limit switches
                PITranslationStage.WaitForIdle(self,i)
        except pipython.GCSError:
                print("Wrong informations or communication already openened")
    def Move(self,Axes,N):
        """
        The Move method move specific axes to target position 

        Parameters
        ----------
        Axes : Axes the user wants to move
        N : Target Position

        Returns
        -------
        None.

        """
        try:
            if int(Config.PYLimitUP[int(Axes)-1])>>int(Axes)>>int(Config.PYLimitDown[int(Axes)-1]):         # Check if we are int he limits    
                self.pidevice.MOV(Axes,N)                                                                   # Move the axes 
                PITranslationStage.WaitForIdle(self,Axes)                                                   # Wait until the movement is finished
            else:
                print('Values out of the limits')
        except pipython.GCSError:
            pass
        
    def Position(self,Axes):
        """
        The Position method return the current position of the axes 

        Parameters
        ----------
        Axes : Axes the user wants to know coordinates
        
        Returns
        -------
        None.

        """
        self.State["Coord"+str(Axes)]=self.pidevice.qPOS(Axes)          # Save the position of current axes in the dictionnary
    
    def WaitForIdle(self,Axes):
        """
        The WaitForIdle method wait until the movement is finished.
        The idea is to check if the current position is diffferent with
        the position one second ago. If they are the same, we stop the loop
        and send new instructions

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        for i in range (0,20):                               # Do 20 iterations so we wait 20 seconds max
           PITranslationStage.Position(self,Axes)            # Check the current position
           A=self.State["Coord"+str(Axes)]                   # Save the result in A
           time.sleep(1)                                     # Wait 1 sec
           PITranslationStage.Position(self,Axes)            # Check the new position
           B=self.State["Coord"+str(Axes)]                   # Save the result in B
           if A==B:                                          # If the position didn't change, the movement is finished
               break                                         # We break the loop
           
    def CloseConnection(self):
        """
        The Close Connection method, close the connection with each device

        Returns
        -------
        None.

        """
        try:
            self.pidevice.CloseConnection()                  # Close the connection with every device
        except pipython.GCSError:
            print("Can't close the communication")
        
Test=PITranslationStage()
Test.OpenConnectionUSB()
Test.OpenConnectionUSB()
Test.Move("1",5.12266)
Test.Move("1",8.3)
Test.CloseConnection()
Test.CloseConnection()
        

        