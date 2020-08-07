-------------------------------------------------------------------------

If you want to understand how to use the class **CNC** (from Driver.py). :

-------------------------------------------------------------------------

1. Give the configurations of each of your devices in the file Config.py
	- Port where the 3d-mill is pluged → PortPrinter
	
2. Import the class in another script (imported in Wells.py) or go under 'if __name__=='__main__'':
	
3. Initialize the class :
	VariableName=CNC(Config.PortPrinter)
	
4. Open the connection with the 3d-mill :
	VariableName.OpenConnection()
	
5. Move the 3d-mill where you want:
	VariableName.Move(G,X,Y,Z)
	- G is 90 or 91 depending if you want to move in relative (91) or absolute (90)
	- X,Y and Z are given in millimeters

6. Close the connection with the 3D printer:
	VariableName.CloseConnection()
	
--------------------------------------------------------------------------

If you want to understand how to use the class **Wells.** :

--------------------------------------------------------------------------

1. Give the configurations of each of your devices in the file Config.py
	- Number of Wells in width (Axis Y) → NbWellsWidth
	- Number of Wells in length (Axis X) → NbWellsLength
	- Distance between the center of 2 wells in width (in mm) → DifferenceW
	- Distance between the center of 2 wells in length (in mm)→ DifferenceL
	
2. Import the class in an other script or go under 'if __name__=='__main__'':
	
3. Initialize the class :
	VariableName=Wells()

4. Move the 3d-mill to target well:
	VariableName.MoveWells(X) (X is the number of the wells)

5. Close the connection with the MS2000:
	VariableName.CloseConnection()
	

When you will execute the script you will receive a message asking you if you are above the Wells 1.
If you are not, go check the end of this document.

If you don't want to see this message every time:
	- Open Wells.py
	- Go to line 48 (You should see "Wells.Wells_1(self)")
	- Put a "#" in front of the line
	- The line should be grey now
Don't forget to delete the character at the end of your manipulation 

If you encounter a problem with the 3d-mill coordinates:

----------------------------------------------------------------------

Prob : The coordinates of the origins(0,0,0) has changed or I'm not above the Wells 1

---------------------------------------------------------------------

Sometimes, for example if the electricty shutdowns when the 3d-mill is working, the coordinates of the origins will change.
I don't know why. But don't panic this is not a huge problem to solve because all the programs are made to work in relative 
coordinates. So the goal here is basically to go to the point where your Wells 1 is and to start you manipulation.

How to do ?

	- Open the file "Driver.py" with spyder 
	- Go at the end of the program
	- Under "if __name__ =="__main__":", write your instructions.
	- For example, if you want to move in relative coordinates X=+5mm Y=-3mm Z=+2mm, your instructions should look like this:
		- if __name__ == "__main__":
    			cnc = CNC(Config.PortPrinter)
    			cnc.OpenConnection()
    			cnc.Move(91,5,-3,2)
    			cnc.CloseConnection()
	- Then execute your script (press F5)
	
The X,Y,Z axis are written on the 3d-mill.
Use low amplitude movements if you want to be sure you don't damage the device.
Be sure the needle is above the wells before moving in X,Y.
If you want to move only on Z you can write "cnc.Move(91,0,0,2)"for example.
