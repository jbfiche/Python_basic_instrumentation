This file explains how to use the class Driver. 

1. Give the configurations of each of your devices in the file Config.py
	- Port where the 3d-mill is pluged → PortPrinter
	
2. Import the class in an other script (imported in Wells.py) or go under 'if __name__=='__main__'':
	
3. Initialize the class :
	VariableName=CNC(Config.PortPrinter)
	
4. Open the connection with the 3d-mill :
	VariableName.OpenConnection()
	
5. Move the 3d-mill where you want:
	VariableName.Move(G,X,Y,Z)
	# G is 90 or 91 depending if you want to move in relative (91) or absolute (90)
	# X,Y and Z are given in millimeters

6. Close the connection with the MS2000:
	VariableName.CloseConnection()
	
