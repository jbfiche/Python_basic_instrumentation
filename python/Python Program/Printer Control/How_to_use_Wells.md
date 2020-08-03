This file explains how to use the class Wells. 

1. Give the configurations of each of your devices in the file Config.py
	- Number of Wells in width (Axis Y) → NbWellsWidth
	- Number of Wells in length (Axis X) → NbWellsLength
	- Difference between the center of 2 wells in width → DifferenceW
	- Difference between the center of 2 wells in length → DifferenceL
	
2. Import the class in an other script or go under 'if __name__=='__main__'':
	
3. Initialize the class :
	VariableName=Wells()

4. Move the 3d-mill to target well:
	VariableName.MoveWells(X) (X is the number of the wells)

5. Close the connection with the MS2000:
	VariableName.CloseConnection()
	
When you will execute the script you will recieve a message asking you if you are above the Wells 1.
If you are not, go check the file "3d-mill coordinates" in problems.

If you don't want to see this message every time:
	- Open Wells.py
	- Go to line 48 (You should see "Wells.Wells_1(self)")
	- Put a "#" in front of the line
	- The line should be grey now
Don't forget to delete the character at the end of your manipulation 
