#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 15:12:48 2020

@author: fiche
"""

from pyueye import ueye
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import cv2
import numpy as np
# import time

class CameraThorlabs(qtc.QObject, qtg.QPixmap):
    
    cam_initialized = qtc.pyqtSignal(str)
    cam_acquiring = qtc.pyqtSignal(qtg.QPixmap)
    
    # Define the __init__ construction method
	# ---------------------------------------
    
    def __init__(self, camID):
        super().__init__()
        
        # Define the variables that will be used to retrieve the properties
        # of the camera (generic dictionnaries from ueye)
        # -----------------------------------------------
        
        self.hcam = ueye.HIDS(camID) # 0 for the first available camera - 1-254 when we already have a specified ID
        self.sensor_info = ueye.SENSORINFO()
        self.cam_info = ueye.CAMINFO()
        self.rectAOI = ueye.IS_RECT()
        self.pcImageMemory = ueye.c_mem_p()
        self.MemID = ueye.int()
        self.pitch = ueye.INT()
        
    @qtc.pyqtSlot(int)    
    def open_connection(self, camID):
        
        """
        Function taking care of the Thorlabs camera initialization. 

        Parameters
        ----------
        camID : int - indicate the handle of the camera we want to intialize. 

        """
        
        # Starts the driver and establishes the connection to the camera
        # --------------------------------------------------------------
        
        self.hcam = ueye.HIDS(camID)
        
        Init = ueye.is_InitCamera(self.hcam, None)
        if Init != ueye.IS_SUCCESS:
            print("is_InitCamera ERROR - make sure the camera is properly connected")
            self.cam_initialized.emit('')
            return
            
        # Reads out the data hard-coded in the non-volatile camera memory and 
        # writes it to the data structure that cInfo points to
        # ----------------------------------------------------
        
        read_cam_info = ueye.is_GetCameraInfo(self.hcam, self.cam_info)
        if read_cam_info != ueye.IS_SUCCESS:
            print("is_GetCameraInfo ERROR")
            self.cam_initialized.emit('')
            return

        # You can query additional information about the sensor type used in 
        # the camera
        # ----------
        
        read_sensor_info = ueye.is_GetSensorInfo(self.hcam, self.sensor_info)
        if read_sensor_info != ueye.IS_SUCCESS:
            print("is_GetSensorInfo ERROR")
            self.cam_initialized.emit('')
            return

        # Reset buffer and all the display parameters to the default values
        # -----------------------------------------------------------------

        reset = ueye.is_ResetToDefault(self.hcam)
        if reset != ueye.IS_SUCCESS:
            print("is_ResetToDefault ERROR")
            self.cam_initialized.emit('')
            return

        # Set display mode to DIB - the image is directly saved on the RAM
        # ----------------------------------------------------------------

        ueye.is_SetDisplayMode(self.hcam, ueye.IS_SET_DM_DIB)
        
        # Set the color mode according to the sensor properties
        # -----------------------------------------------------
        
        if int.from_bytes(self.sensor_info.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
            # for color camera models use RGB32 mode
            self.m_nColorMode = ueye.IS_CM_BGRA8_PACKED
            self.nBitsPerPixel = ueye.INT(32)
            self.bytes_per_pixel = int(self.nBitsPerPixel / 8)
            self.color_mode = 'RGB'
        
        elif int.from_bytes(self.sensor_info.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
            # for color camera models use RGB32 mode
            self.m_nColorMode = ueye.IS_CM_MONO8
            self.nBitsPerPixel = ueye.INT(8)
            self.bytes_per_pixel = int(self.nBitsPerPixel / 8)
            self.color_mode = 'Monochrome'
        
        else:
            print('Error : the camera type is unknown.')
            self.cam_initialized.emit('')
            return
        
        # Define a dictionary with the main properties of the camera selected
        # -------------------------------------------------------------------
    
        ueye.is_AOI(self.hcam, ueye.IS_AOI_IMAGE_GET_AOI, self.rectAOI, ueye.sizeof(self.rectAOI))
        
        self.Properties = {'Camera sensor model (from IDS)': self.sensor_info.strSensorName.decode('utf-8'),
                      'Camera s/n': self.cam_info.SerNo.decode('utf-8'),
                      'Color mode': self.color_mode,
                      'Image width': int(self.rectAOI.s32Width),
                      'Image height': int(self.rectAOI.s32Height),
                      }
            
        # Indicate that the initialization procedure was completed
        # --------------------------------------------------------
        
        print('Success : Thorlabs camera was found and initialized')
        self.cam_initialized.emit(self.Properties['Camera s/n'])
       
        
    @qtc.pyqtSlot()
    def init_acquisition(self):
        
        """
        Allocate the computer memory according to the size of the image and 
        start the acquisition.

        """
        
        # Allocate memory for the acquisition
        # -----------------------------------
        
        self.width = self.rectAOI.s32Width
        self.height = self.rectAOI.s32Height
        Allocate_memory = ueye.is_AllocImageMem(self.hcam, self.width, self.height,
                                                self.nBitsPerPixel, self.pcImageMemory, self.MemID)
        
        if Allocate_memory != ueye.IS_SUCCESS:
            print("is_AllocImageMem ERROR")
            return
        else:
            # Makes the specified image memory the active memory
            Allocate_memory = ueye.is_SetImageMem(self.hcam, self.pcImageMemory, self.MemID)
            if Allocate_memory != ueye.IS_SUCCESS:
                print("is_SetImageMem ERROR")
                return
            else:
                # Set the desired color mode
                Color_mode = ueye.is_SetColorMode(self.hcam, self.m_nColorMode)
                
        # Activates the camera's live video mode (free run mode)
        # ------------------------------------------------------
        
        Launch_capture = ueye.is_CaptureVideo(self.hcam, ueye.IS_DONT_WAIT)
        if Launch_capture != ueye.IS_SUCCESS:
            print("is_CaptureVideo ERROR")
            return

        # Enables the queue mode for existing image memory sequences
        nRet = ueye.is_InquireImageMem(self.hcam, self.pcImageMemory, self.MemID, 
                                       self.width, self.height, self.nBitsPerPixel, self.pitch)
        if nRet != ueye.IS_SUCCESS:
            print("is_InquireImageMem ERROR")
            return
        
        # Launch the live acquisition
        # ---------------------------
        
        self.acquire()
        
    
    def acquire(self):
        
        
        # while(nRet == ueye.IS_SUCCESS):

        # In order to display the image in an OpenCV window we need to extract the 
        # data of our image memory, reshape it as a numpy array and define it as a 
        # cv2 object.
        # -----------
    
        array = ueye.get_data(self.pcImageMemory, self.width, self.height, self.nBitsPerPixel, 
                              self.pitch, copy=False)
    
        # bytes_per_pixel = int(nBitsPerPixel / 8)
    
        frame = np.reshape(array,(self.height.value, self.width.value, self.bytes_per_pixel))
        frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
    
        # # ...resize the image by a half
        # frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
        
        #---------------------------------------------------------------------------------------------------------------------------------------
        #Include image data processing here
        #---------------------------------------------------------------------------------------------------------------------------------------
    
        frame = qtg.QImage(frame, frame.shape[1], frame.shape[0], qtg.QImage.Format_RGB888)
        frame = qtg.QPixmap.fromImage(frame)
        self.cam_acquiring.emit(frame)
        print(frame)
        
    @qtc.pyqtSlot()     
    def close_connection(self):
        
        """
        Close the connection with the Thorlabs camera and release the handle 
        as well as the memory usage

        """
        ueye.is_FreeImageMem(self.hcam, self.pcImageMemory, self.MemID)
        ueye.is_ExitCamera(self.hcam)
        print('Connection to the camera was closed')
        
        
if __name__ == "__main__":
    
    cam = CameraThorlabs(0)
    cam.open_connection()
    cam.close_connection()
    
