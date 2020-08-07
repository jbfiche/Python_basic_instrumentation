---------------------------------------------------------------------------------

This file explains how to use the class **Valve**. Valve used: Hamilton MVP serial:

---------------------------------------------------------------------------------

1. Give the configurations of each of your devices in the file Config.py
	- Number of valve used → NbofValve
	- Port where the first valve is pluged → PortValve
	- Configuration of the valves (number of positions available on the valve, e.g 8). 
	If there are more than one valve, indicate the configuration of each valve in the same order than the adress (a, b, c ...)→ ValveConfigPosition[]
	
2. Import the class in an other script or go under 'if __name__=='__main__'':
	
3. Initialize the class :
	VariableName=Valve()
	
4. Open the connection with the valve :
	VariableName.OpenConnection()
	
5. Select the position you want for target valve :
	VariableName.ValveRotation("b",5)
	
--------------------------------------------------------------------------------

If you encounter a problem with the valve Hamilton serial MVP :

--------------------------------------------------------------------------------

Prob : The valve makes a noise (like "bip" "bip") then stop working

When the valve finish an action, sometimes it will make noise and stop working. The problem is the valve recieved a new instruction when it was already working.
Don't panic. First, be sure the manipulation is finished or end it by yourself. To stop the noise, just press one of the two arrows in front of the device.

Now you must found what causes the problem. Some advices that can help you:
	- Where the valve stopped ? If your instructions are :
		- Test=Valve()
		- Test.OpenConnection()
		- Test.ValveRotation("a",6)
		- Test.ValveRotation("a",2)
		- Test.ValveRotation("a",4)
		- ........
	and the valve is stopped in position 2, that means the device receive the instruction (ValveRotation("a",4)) when it was doing the instruction (ValveRotation("a",2))
	If the same position occurs more than one times in your program, try to count wich one is the last realized
	
	- When you have found what instruction is the problem, you must now solve the problem. In the class "Valve", the "ValveRotation" method uses the "WaitForIdle" method
	to be sure the actual instruction is finished before sending the next one. But, maybe there is a problem with this method (bad communication with the device,....)
	So, what you can try is to add some command time.sleep in your program to see if the problem came from the WaitForIdle method. For example, your code will look like this :
		- .........
		- Test.ValveRotation("a",6)
		- time.sleep(5)
		- Test.ValveRotation("a",2)
		- time.sleep(5)
		- ..........
		
The problem is NOT SOLVED : In this case, the problem came from somewhere else. Be sure you have done the "OpenConnection" method before sending any command.
Be sure your instructions correspond to your valve configuration (file : Config.py). Be sure the valve assignation is correct (First valve is "a"). Check if 
the LED in the back correspond to your parameters (baudrate,.....)

The problem is SOLVED : In this case, the problem came from the "WaitForIdle" method. So, instead of waiting, the method seems to be sending the new instruction.
This method uses the "Status" method to check the current state of each valve. First, check if the number of valve (NbofValve) is correct in the file Config.py.
If a valve is idle, it will send an "Y". So the idea in the method WaitForIdle is while all the valve are not idle (sending "Y") we wait.
So maybe one of the valve is always sending "Y" instead of "*" when it is busy.


