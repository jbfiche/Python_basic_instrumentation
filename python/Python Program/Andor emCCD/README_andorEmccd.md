------------------------------------------------------------------------

This file explains how to use the andorEmccd class and how to modify it:

------------------------------------------------------------------------

The script **andorEmccd.py** in the folder andorEmccd contains the classes used to control the camera. There are two classes in the script :

- **LibInstance** : instantiation of the library (atmcd32d.dll or atmcd64d.dll) and definition of all the methods that will be called from the library
- **AndorEmccd** : class used to control the camera after loading the library

The class **AndorEmccd** is used in the script example.py. In this file, you will found some examples illustrating
how to use the methods and how to communicate with the Andor camera.

You may have to create new methods in the script andorEmccd.py as I did. This a short tutorial to explain how:
(Example: The method get_status)

1. Read the characteristics of the function corresponding to your method in the SDK manual:
	For example, we want to add the function **GetStatus(int*status)**. This function has only one output parameter. The current status of our device will be returned as an int.

2. Call the function and save it into a variable: 

- In andorEmccd.py you can see all the function called from the library between lines 110 and 155.

- Add the one you want to create to this list :

  ```python
  self.get_status=wrapper(dll.GetStatus,[POINTER(c_int)])
  ```

  ​	Name of the variable → self.get_status
  ​	Call of the function → dll.GetStatus
  ​	Output → [POINTER(c_int)] (POINTER() means you want to read the output)
  ​	

3. Create your method:

   ```python
   def get_status(self):
    		status=c_long()                                    
           # Define the type of status c_long and c_int are equivalent 
    		self.lib.get_status(ctypes.byref(status))          
           # Call the variable we defined earlier and ask the device his current status
    		Status=str(status)                                 
           # Read the status and stock it into a string
    		if Status=="c_long(20073)":                        
           # Depending of the status we can say to the user if the camera is working or not
        			print("Idle (20073)")
    		elif Status=="c_long(20072)":
        			print("Running (20072)")
    		else:
        			print("Error No:"+Status)
   ```
------------------------------------------------------------------------------   
   
If you encounter a problem with the AndorCamera :

------------------------------------------------------------------------------

Prob : Unicode Error (Specific to windows ?)

When you give a path for your spool for example, you will have to write it like this :

	C:\\Users\\......\\....\\
	
If you write the path as usual: C:\Users\....\.....\ python will expect numbers after \U

---------------------------------

Prob : 1 argument expected (4 given)

In this case, the problem is the number of arguments your function can handle is wrong.

For example, the function SetShutters needs 4 arguments:

	SetShutters(int ttlType,int mode,int closingTime,int openingTime) (All of the arguments are int)
	
But if you write "self.set_shutter = wrapper(dll.SetShutter, [c_int])", your variable will expect only one argument.

So, this is wrong. The correct command is :

	self.set_shutter = wrapper(dll.SetShutter, [c_int,c_int,c_int,c_int])
	
---------------------------------

Prob : Wrong C_types

In this case, one of your c_types is wrong. You can easily find some data about c_types on the internet 
but I can give you some tips:
	1. c_char and c_char_p are different. c_char means you have only one character in your string.
	c_char_p means you have more than one character in your string (in the SDK c_char_p correspond 
	to char*name).
	2. c_int and c_long are both int in terms of Python type. The difference is c_int is for an int 
	between -32768 and 32767. c_long is for an int between -2147483648 and 2147483647.
	
   
