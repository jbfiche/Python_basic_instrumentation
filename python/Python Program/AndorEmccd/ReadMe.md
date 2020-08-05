System Tested : Windows

Works with : Python 3.6;3.7

Don't works with : Python 3.8

The script andorEmccd.py in the folder andorEmccd contains the class wich allows you to control the device.

This class is used in the script example.py. In this file, you will found some examples to understand
how to use the methods and how to interact with the Ancor camera.

You may have to create new method in the script andorEmccd.py as I did. This a short tutorial to explain how:
(Example: The method get_status)
	1.Read the caracteristics of the function corresponding to your method in the SDK :
		In our case the function is : GetStatus(int*status). This means we have only one parameter.  
		This function will return the current status of our device as an int.
	
	2.Call the function and save it into a variable:
		In andorEmccd.py you can see all the function called between line 110 and line 155
		Add the one you want to create to this list :
			self.get_status=wrapper(dll.GetStatus,[POINTER(c_int)])
		Name of the variable → self.get_status
		Call of the function → dll.GetStatus
		Read the output → [POINTER(c_int)] (POINTER() means you want to read the output)
		
	3. Create your method:
		def get_status(self):
        		status=c_long()                                    # Define the type of status c_long and c_int are equivalent 
        		self.lib.get_status(ctypes.byref(status))          # Call the variable we defined earlier and ask the device his current status
        		Status=str(status)                                 # Read the status and stock it into a string
        		if Status=="c_long(20073)":                        # Depending of the status we can say to the user if the camera is working or not
            			print("Idle (20073)")
        		elif Status=="c_long(20072)":
            			print("Running (20072)")
        		else:
            			print("Error No:"+Status)
