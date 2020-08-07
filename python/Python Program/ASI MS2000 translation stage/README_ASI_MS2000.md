This file explains how to use the class MS2000. 

1. Give the configurations of each of your devices in the file Config.py
	- Port where the MS2000 is pluged → PortMS2000
	
2. Import the class in an other script or go under 'if __name__=='__main__'':
	
3. Initialize the class :
	VariableName=MS2000()
	
4. Open the connection with the MS2000 :
	VariableName.OpenConnection()
	
5. Depending of what you want to do call the specific method :
	1. If you want to move in relative coordinates:
		- VariableName.MoveREL(X,Y) (X and Y are in micrometers)
	2. If you want to move in absolute coordinates:
		- VariableName.MoveABSOL(X,Y) (X and Y are in micrometers)
	3. If you want to save your current position as an ROI:
		- VariableName.MemorizeROI()
	4. If you want to move to all the ROI saved in the file:
		- VariableName.GOTOROI()
	5. If you want to delete all the ROI saved :
		- VariableName.DELETEALLROI()
	6. If you want to change the speed:
		- VariableName.Speed(X,Y)
	7. If you want to change the brightness:
		- VariableName.LED(brightness) (brightness must be between 0 and 99)

6. Close the connection with the MS2000:
	VariableName.CloseConnection()
	
