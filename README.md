# Python_basic_instrumentatiokn

FILE IN THIS FOLDERS:

--------------------

Config : Parameters of each device (Printer,Wells,Valve). Read it before using any program to be sure that the parameters correspond to your devices. You can change their value but don't change the name of the variable. You can add new variable if you need to. To call a variable in an other script you have to:
	import Config (if your script is in the same deposit as the file Config.py)
	write your variable like this : Config.$NameOfYourVariable"

----------------------------------------------------

Driver : Drivers for the 3D-mill.Contains all the methods to interact with the device. They are basic functions used in the script "Wells.py".
Methods in Driver :
	-Open/Close Connection
	-Status
	-WaitForIdle
	-Move
If you want further informations about the methods check the file himself

----------------------------------------------------

log_file : Historic of instruction send to the 3d-mill. If the printer seems to be not working when u send a list of instruction, chek the file to be sure there is not a problem with your script. For example if u open two times the communication with the device.

----------------------------------------------------

Wells : Program to move the 3D-mill to specific wells. This script use the class CNC created in Driver to move the 3d-mill.
Methods in Wells:
	-Wells_1
	-CoordWells
	-MoveWells
	-CheckValue
If you want further informations about the methods check the file himself 

----------------------------------------------------

Valve : Contains all the methods to interact with one or more valve.
Methods in Valve:
	-Open Connection
	-Status
	-WaitForIdle
	-ValveRotation
If you want further informations about the methods check the file himself

----------------------------------------------------

Problem : File where you can find some solutions to some problems I have encountered during the developement of this scripts

