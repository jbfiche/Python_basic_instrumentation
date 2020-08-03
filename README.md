# Python_basic_instrumentation

FILE IN THIS FOLDERS:

--------------------

Config : Parameters of each device (Printer,Wells,Valve). Read it before using any program to be sure that the parameters correspond to your devices. You can change their value but don't change the name of the variable. You can add new variable if you need to. To call a variable in an other script you have to:
	- import Config (if your script is in the same deposit as the file Config.py)
	- write your variable like this : Config.$NameOfYourVariable"

----------------------------------------------------

Driver : Drivers for the 3D-mill.Contains all the methods to interact with the device. They are basic functions used in the script "Wells.py".
Methods in Driver :
	- Open/Close Connection (Open or close the communication with the device)
	- Status (Get the current state of the device)
	- WaitForIdle (Wait until the device has finished his action)
	- Move (Move the device to target coordinates)

Wells : Program to move the 3D-mill to specific wells. This script use the class CNC created in Driver to move the 3d-mill.
Methods in Wells:
	- Wells_1 (Ask the user if the 3D-mill is above the Wells 1)
	- CoordWells (Calculate the coordinates of the wells)
	- MoveWells (Move to the wells depending of the number given by the user)
	- CheckValue (Check if the value of the wells give by the user is correct)

----------------------------------------------------

log_file : Historic of instruction send to the 3d-mill. If the printer seems to be not working when u send a list of instruction, chek the file to be sure there is not a problem with your script.
For example if u open two times the communication with the device.

----------------------------------------------------

Valve : Contains all the methods to interact with one or more valve.
Methods in Valve:
	- Open Connection (Open the communication with the device)
	- Status (Get the current state of the device)
	- WaitForIdle (Wait until the device has finished his action)
	- ValveRotation (Rotate the valve to target position)

----------------------------------------------------

MS2000 : Drivers for the translation plate (MS2000). Contains all the methods to interact with the device and to save the Range Of Interest :
Methods in MS2000:
	- Open/Close Connection (Open or close the communication with the device)
	- Status (Get the current state of the device)
	- WaitForIdle (Wait until the device has finished his action)
	- MoveREL (Move the device to target coordinates in relative)
	- MoveABSOL (Move the device to target cooridnates in absolute)
	- AxisPosition (Return the current axis positions of the device)
	- MemorizeROI (Save the coordinates of a Range Of Interest)
	- GoToROI (Move to all the ROI saved before)
	- Speed (Set the speed of the device)
	- Brightness (Set the luminosity of the device)
	
---------------------------------------------------- 
	
Problem : File where you can find some solutions to some problems I have encountered during the developement of this scripts

----------------------------------------------------

Celesta : Folder that contains current development regarding the control of the Celesta Engine Light (Lumencor).

One of the files was created by Bogdan Bintu to control their Celesta through a RG45 cable, it is called "celesta.py". It was used as a base to control our own.
The code called "control_celesta.py" will be used to modulate the lasers in sync with the camera ORCA Flash 4.0 (Hamamatsu) and the filter wheel Lambda 10-3 (Sutter Instruments).
