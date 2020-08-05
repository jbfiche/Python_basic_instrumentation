"""An example of how to take a single image using the AndorEmccd class"""
import time
from andorEmccd import AndorEmccd
import cv2
import numpy as np
SpoolPath='C:\\Users\\admin\\Desktop\\Stage_Aymerick\\python\\Python Program\\AndorEmccd\\'
FileName='Test2'
FrameBufferSize=10
# Mesure en continue

# cam = AndorEmccd()
# cam.get_status()
# try:
#     cam.set_shutter_open(True)
#     cam.set_temperature(20)
#     cam.set_exposure_time(0.1)
#     cam.start_acquisition(single=False)
#     X=0
#     while X!=1:  
#         im = cam.wait_for_image()
#         array=im.astype("uint8")
#         frame = cv2.resize(array,(0,0),fx=1.0, fy=1.0)
#         cv2.imshow("Image",frame)
#         cv2.waitKey(1)
#         cam.get_status()
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cv2.destroyAllWindows()
#     cam.stop_acquisition()   
# except:
#     print("Problème")
#     pass
# cam.set_shutter_open(False)
# cam.get_status()
# cam.close()

#################

#Contrôle que la température varie bien (et quelques autres fonctions)

# cam = AndorEmccd()
# cam._get_preamp_gains()
# cam._get_vertical_shift_speeds()
# cam._get_horizontal_shift_speeds()
# cam.get_horizontal_shift_parameters()
# cam.get_temperature()
# cam.get_acquisition_timings()
# cam.get_all_images()
# cam._get_all_images()
# cam.get_status()
# cam.set_temperature(5)
# for i in range (0,20):
#     cam.get_temperature()
#     time.sleep(10)
# cam.close()

##################

#Spool

cam = AndorEmccd()
cam.set_shutter_open(True)
cam.set_temperature(20)
cam.set_exposure_time(0.1)
cam.set_spool(True,SpoolPath,FileName,FrameBufferSize)
cam.start_acquisition(single=False)
time.sleep(20)
cam.stop_acquisition() 
cam.set_spool(False,SpoolPath,FileName,FrameBufferSize)
cam.set_shutter_open(False)

##################

