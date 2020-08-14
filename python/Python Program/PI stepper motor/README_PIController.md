---------------------------------------------------------------------------------

This file explains how to use the class **PITranslationStage**. 

---------------------------------------------------------------------------------

1. Give the configurations of each of your devices in the file Config.py
	- Name of all the devices → PYName
	- SerialNum of each device → PYID
	- Limit up of each device → PYLimitUP
	- Limit down for each device → PYLimitDown
	- Number of axes → NbofAxes
	
2. Import the class in an other script or go under 'if __name__=='__main__'':
	
3. Initialize the class :
	VariableName=PITranslationStage()
	
4. Open the connection with all the devices :
	VariableName.OpenConnectionUSB()
	
5. Select the position you want for target device :
	VariableName.Move("1",5.1548)
	VariableName.Move("3",8.1565)
	
--------------------------------------------------------------------------------

If you encounter a problem with the PITranslationStage

--------------------------------------------------------------------------------

Prob : Can't find the module "pipython"




