# Python_basic_instrumentation

# List of the files in the folder PROGRAM

--------------------

--------------------

## Configuration file :

**Config.py** : Parameters of each device (Printer,Wells,Valve, etc.). Read it before using any program to be sure that the parameters correspond to your devices. You can change their values but don't change the name of the variables. You can add new variables if you need to. To call a variable in an other script you have to:

 - import Config (if your script is in the same deposit as the file Config.py)
 - write your variable like this : Config.$NameOfYourVariable"

----------------------------------------------------

## 3D Printer control (cnc) :

**Driver.py** : System tested: Windows(10)+Linux(PopOS)   Works with:Python 3.8;3.7 

**Communication method** : serial (package pyserial)

Drivers for the 3D-mill. Define a class called **CNC** design for the control of the 3D printer. It contains all the basic methods to communicate with the device. Those methods are used in the script **Wells.py**.

Methods in **Driver.py** :

 - Open/Close Connection (Open or close the communication with the device)
 - Status (Get the current state of the device)
 - WaitForIdle (Wait until the device has finished his action)
 - Move (Move the device to target coordinates)

**Wells.py** : System tested: Windows(10)+Linux(PopOS)    Works with:Python 3.8;3.7

Program to move the 3D-mill to specific wells (on a eppendorf rack). This script uses the class **CNC** created in **Driver.py** to move the 3d-mill.
A class **Wells** is created with the following methods :

 - Wells_1 (Ask the user if the 3D-mill is above the Wells 1)
 - CoordWells (Calculate the coordinates of the wells)
 - MoveWells (Move to the wells depending of the number given by the user)
 - CheckValue (Check if the value of the wells give by the user is correct)



**log_file **: Historic of the instructions sent to the 3D-mill. If the printer seems to not work when u send a list of instructions, check the file to be sure there is not a problem with your script.
For example if you open twice the communication with the device. 

More information can be found at python/Python Program/3D Printer Control

----------------------------------------------------

## HAMILTON valve used on the merFISH setups :

**Valve.py** : System tested:Windows(10)+Linux(PopOS)    Works with:Python 3.8

**Communication method** : serial (package pyserial)

Defines a class **Valve** that contains all the methods to interact with one or more valve (in daisy chain).
Methods in Valve:

 - Open Connection (Open the communication with the device)
 - Status (Get the current state of the device)
 - WaitForIdle (Wait until the device has finished his action)
 - ValveRotation (Rotate the valve to target position)

More information python/Python Program/Hamilton valve/How_to_use.md

----------------------------------------------------

## ASI translation stage MS2000 :

**DriverMS2000.py**: System Tested:Windows(10)    Works with:Python 3.8

**Communication method** : serial (package pyserial)

Drivers for the translation plate (MS2000). Contains a class called **MS2000** containing all the methods needed to communicate with the device and to save the positions of the selected ROIs. 

Methods in **MS2000**:

 - Open/Close Connection (Open or close the communication with the device)
 - Status (Get the current state of the device)
 - WaitForIdle (Wait until the device has finished its action)
 - MoveREL (Move the device to target coordinates in relative coordinates)
 - MoveABSOL (Move the device to target cooridnates in absolute coordinates)
 - AxisPosition (Return the current axis positions of the device)
 - MemorizeROI (Save the coordinates of a ROI)
 - GoToROI (Move to all the ROI saved before)
 - Speed (Set the speed of the device)
 - Brightness (Set the luminosity of the device - in case there is a LED system attached to the stage, like on the merFISH setup)

More detailed information can be found python/Python Program/ASI MS2000 translation stage/How_to_use.md

----------------------------------------------------

## ANDOR emCCD camera :

**andorEmccd.py** : System Tested:Windows(10)   Works with:Python 3.6;3.7   Doesn't work with:Python 3.8

**Communication method** : need to download and install the emCCD libraries (atmcd32d.dll or atmcd64d.dll) provided by ANDOR

The initial examples where found [here](https://github.com/cjbe/andorEmccd). Depending on whether the system if 32bit or 64bit, the program will use different libraries for the camera (either atmcd32d.dll or atmcd64d.dll). Before starting, make sure that the drivers are properly installed and can be found at the location indicated in the program (see andorEmccd.py, line 52).

Contains the methods to interact with the Andor camera, acquire data and more. All the methods are called from the dll library and are defined/described in the SDK manual. The original script **andorEmccd.py** was modified by Aymerick :

- The internal shutter was not working. It is fixed now.
- A **get_status** method was added
- A**set_spool** method was added.

Check the script **example.py** to understand how to use this class. More information can be found python/Python Program/Andor emCCD/How_to_use.md

----------------------------------------------------

Problem : File where you can find some solutions to some problems I have encountered during the developement of this scripts

----------------------------------------------------

## LUMENCOR CELESTA laser source :

Celesta : Folder that contains current development regarding the control of the Celesta Engine Light (Lumencor).

One of the files was created by Bogdan Bintu to control their Celesta through a RG45 cable, it is called "celesta.py". It was used as a base to control our own.
The code called "control_celesta.py" will be used to modulate the lasers in sync with the camera ORCA Flash 4.0 (Hamamatsu) and the filter wheel Lambda 10-3 (Sutter Instruments).

----

## MEASUREMENT COMPUTING DAQ :

**daq.py** : System Tested:Xubuntu  Works with:Python 3.7 

**Communication method** : In order to communicate with the Measurement Computing acquisition card, a universal library for Linux is available on gitHub [here](https://github.com/mccdaq/uldaq/blob/master/README.md). As usual, this library is actually written in C/C++ and an API (Application Programming Interface) is used to interact directly with this library in Python. 

Note that all files and documentation can be found python/Python Program/Measurement_computing_DAQ/Libraries. The installation procedure works in two steps :

1. Installation of the uldaq library and C/C++ compilers : Follow the instructions described [here](https://github.com/mccdaq/uldaq/blob/master/README.md). Make sure you are running the latest version, else it might not be compatible with your version of Python.
2. Installation of the uldaq API for Python and test of the DAQ : The information regarding the installation are [here](https://pypi.org/project/uldaq/). Installation must be performed in the local environment. The first example analyzed was the function d_in.py that is reading the first available digital port. The function is analyzed in the following python files daq.py and daq_experiment.py. 

-----

## THORLABS CMOS camera (DCC1545) :

All files were installed python/Python Program/Thorlabs camera DCC1545/Doc. A manual of all the cameras can be also be found in the same folder.

## Thorlabs sdk - NOT WORKING

The CMOS camera from Thorlabs was tested on the computer. This model is monochrome with a 1280x1024 pixels sensor. The SDK/ C/C++ libraries for Linux can be found [here](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=ThorCam).

In order to install a Python wrapper, the following sdk needs to be installed as well. Follow theses instruction:

- move to your Python/Conda virtual environment
- cd to the folder containing the Python wrapper (for this computer it is located [here](python/Python Program/Thorlabs camera DCC1545/Doc/Scientific_Camera_Interfaces_Linux-1.3/Python_SDK)
- run `python -m pip install thorlabs_tsi_camera_python_sdk_package.zip`

Installation went well though in the end it was impossible to detect any camera on the computer... apparently this model of camera is not supported.

## PyuEye and drivers

Since our DCC-1545 camera was not detected using the Thorlab sdk, another methods was described in the (python/Python Program/Thorlabs camera DCC1545/Doc/DCU223C-Manual.pdf), p.61. Following the link indicated for Linux, it is possible to download the Linux drivers for the camera (see python/Python Program/Thorlabs camera DCC1545/Doc/uEye_Linux_382_64Bit/uEye_Linux_382_64Bit/ for the drivers).

Following the readme file, install the **uEye SDK for Linux**. In order to check if the installation worked :

- start a new terminal with super-user right
- Use the following command to start the Daemon : `/etc/init.d/ueyeusbdrc start`
- In order to test whether there is a camera connected to the PC, type `ueyesetid -d`. If there is a camera, the device should appear with the right serial #. Interestingly, the model of camera is not DCC1545 but UI-1540ME-M and can be found directly on the **IDS (imaging development systems Gmbh) website**. 
- In order to close the program  type : `/etc/init.d/ueyeusbdrc stop`.

 A specific API to interface uEye with Python can be downloaded [here](https://pypi.org/project/pyueye/). In order to found the manual and examples, you need to download the files available on the webpage. A very simple example can also be downloaded from the IDS website and can be found in the folder python/Python Program/Thorlabs camera DCC1545/Doc/pyueye/uEye_SimpleLive_PyuEye_OpenCV. It was tested and allow for a proper detection of the DCC1545 camera.

Finally, the manual with all the functions can be found [here](https://en.ids-imaging.com/download-details/AB.0010.1.25600.23.html?os=linux&version=&bus=64&floatcalc=) but you need to have an account to access this webpage. 

---------------------------------------------------------

## PI stepper motor controller

**PIController.py**: System Tested:Windows(10) Works with:Python 3.8  PI Tested:C-663

**Comunication method** : (USB). Need to install pipython by using the CD.

Drivers for the PI stepper motor controller. Contains a class called **PITranslationStage** containing all the methods needed to communicate with the device. 

Methods in **PIController**:

 - Open/Close Connection (Open or close the communication with the device)
 - WaitForIdle (Wait until the device has finished his action)
 - Move (Move the device to target coordinates in absolute coordinates)
 - Position (Return the current axis positions of the device)
 
More detailed information can be found python/Python Program/PI stepper motor controller/README_PIController.md










