"""
This file contains examples to understand how to use some functions
"""
import time
from andorEmccd import AndorEmccd
import cv2

SpoolPath='C:\\Users\\admin\\Desktop\\Stage_Aymerick\\python\\Python Program\\AndorEmccd\\'                        # Path to the folder wher you want to save your data (in case of spooling)
FileName='Acquisition_1'                                                                                           # Name of your file
FrameBufferSize=10                                                                                                 # Size of the frame buffer

# Continuous acquisition

# cam = AndorEmccd()                                                                      # Initialize the device
# cam.get_status()                                                                        # Print the current status of the camera (Idle if there is no acquisition and Running if there is one)
# try:
#     cam.set_shutter_open(True)                                                          # Open the shutter of the camera
#     cam.set_temperature(20)                                                             # Set the temperature
#     cam.set_exposure_time(0.1)                                                          # Set the time of exposure 
#     cam.start_acquisition(single=False)                                                 # Start the acquisition (if Single=True → One acquisition; if Single=False → Continuous acquisition)
#     X=0
#     while X!=1:                                                                         # We want to see the current image until the user decide to stop
#         im = cam.wait_for_image()                                                       # Take the last image (numpy array)
#         array=im.astype("uint8")                                                        # Change the data type in the numpy array 
#         frame = cv2.resize(array,(0,0),fx=1.0, fy=1.0)                                  # Resize our images (if you want something 2 times bigger you can write fx=2.0 and fy=2.0)
#         cv2.imshow("Image",frame)                                                       # Show the image
#         cv2.waitKey(1)                                                                  # The function waitKey waits for a key event infinitely (when delay < 0 ) or for delay milliseconds,
#         cam.get_status()                                                                # when it is positive. You MUST put this function or your windows will crashes 
#         if cv2.waitKey(1) & 0xFF == ord('q'):                                           # If the user press q (you may have to spam it), stop the loop
#             break
#     cv2.destroyAllWindows()                                                             # We close all of the windows 
#     cam.stop_acquisition()                                                              # We stop the current acquisition
# except:
#     print("Something wrong happened")
#     pass
# cam.set_shutter_open(False)                                                             # Close the shutter of the camera
# cam.get_status()

#################

# Check if the temperature is changing

# cam = AndorEmccd()                                                                      # Initialize the device 
# cam.set_temperature(5)                                                                  # Set the temperature
# for i in range (0,20):                                                                  # Check the temperature every 10 seconds
#     cam.get_temperature()
#     time.sleep(10)

##################

# Spool the data in a specific folder

#cam = AndorEmccd()                                                                      # Initialize the device
#cam.set_shutter_open(True)                                                              # Open the shutter of the camera
#cam.set_temperature(20)                                                                 # Set the temperature
#cam.set_exposure_time(0.1)                                                              # Set the time of exposure
#cam.set_spool(True,SpoolPath,FileName,FrameBufferSize)                                  # Start the spool if True    
#cam.start_acquisition(single=False)                                                     # Start the acquisition (ALWAYS start the acquisition after the sppoling)
#time.sleep(20)                                                                          # Wait some time to acquire data
#cam.stop_acquisition()                                                                  # Stop the acquisition
#cam.set_spool(False,SpoolPath,FileName,FrameBufferSize)                                 # Stop the spool if False
#cam.set_shutter_open(False)                                                             # Close the shutter

##################

