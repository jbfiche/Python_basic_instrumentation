#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:21:43 2020

@author: marion
using the work of Bogdan Bintu
"""

import urllib.request
import traceback

def lumencor_httpcommand(command = 'GET IP',ip = '192.168.201.200'):
    """
    Sends commands to the lumencor system via http.

    """
    command_full = r'http://'+ip+'/service/?command='+command.replace(' ','%20')
    with urllib.request.urlopen(command_full) as response:
        message = eval(response.read()) # the default is conveniently JSON so eval creates dictionary
    return message

class LumencorLaser(object):
    """
    This controls a lumencor object (default: Celesta) using HTTP.
    Please connect the provided cat5e, RJ45 ethernet cable between the PC and Lumencor system.
    """
    def __init__(self, **kwds):
        """
        Connect to the Lumencor system via HTTP and check if you get the right response.
        """
        self.on = False
        self.ip = kwds.get('ip', '192.168.201.200')
        self.laser_id = str(kwds.get('laser_id', 0))
        [self.pmin, self.pmax] = 0,1000
#        try:
#            # See if the system returns back the right IP.
#            self.message = self.getIP()
#            assert (self.message['message'] == 'A IP '+self.ip)
#            assert (int(self.laser_id)<self.getNumberLasers())
#            self.live = True
#        except:
#            print(traceback.format_exc())
#            self.live = False
#            print("Failed to connect to Lumencor Laser at ip:", self.ip)

        if self.live:
            [self.pmin, self.pmax] = self.getPowerRange()
            self.setExtControl(True)
            if (not self.getLaserOnOff()):
                self.setLaserOnOff(False)

    # def getNumberLasers(self):
    #     """
    #     Returns the number of lasers inside the celesta
    #     """
    #     self.message = lumencor_httpcommand(command ='GET NUMCH', ip=self.ip)
    #     laser_num = self.message['message'].split(' ')[2:]
    #     return laser_num
   
    def getColor(self):
        """Returns the color of the current laser"""
        self.message = lumencor_httpcommand(command ='GET CHMAP', ip=self.ip)
        colors = self.message['message'].split(' ')[2:]
        return colors[int(self.laser_id)]
    
    def getIP(self):
        self.message = lumencor_httpcommand(command = 'GET IP', ip=self.ip)
        return self.message
    
    def getExtControl(self):
        """
        Return True/False the lasers can be controlled with TTL.
        """
        self.message = lumencor_httpcommand(command = 'GET TTLENABLE', ip=self.ip)
        response = self.message['message']
        return response[-1]=='1'
    
    def setExtControl(self, mode):
        """
        Turn on/off external TTL control mode.
        """
        if mode:
            ttl_enable = '1'
        else:
            ttl_enable = '0'
        self.message = lumencor_httpcommand(command = 'SET TTLENABLE '+ttl_enable,ip=self.ip)
        
    def getLaserOnOff(self):
        """
        Return True/False the laser is on/off.
        """
        self.message = lumencor_httpcommand(command = 'GET CH '+self.laser_id, ip=self.ip)
        response = self.message['message']
        self.on = response[-1]=='1'
        return self.on
    
    def setLaserOnOff(self, on):
        """
        Turn the laser on/off.
        """
        if on:
            self.message = lumencor_httpcommand(command = 'SET CH '+self.laser_id+' 1', ip=self.ip)
            self.on = True
        else:
            self.message = lumencor_httpcommand(command = 'SET CH '+self.laser_id+' 0', ip=self.ip)
            self.on = False
        # print("Turning On/Off", self.on, self.message)

    def getPowerRange(self):
        """
        Return [minimum power, maximum power].
        """
        max_int =1000 # default
        self.message = lumencor_httpcommand(command = 'GET MAXINT', ip=self.ip)
        if self.message['message'][0]=='A':
            max_int = float(self.message['message'].split(' ')[-1])
        return [0, max_int]

    def getPower(self):
        """
        Return the current laser power.
        """
        self.message = lumencor_httpcommand(command = 'GET CHINT '+self.laser_id, ip=self.ip)
        response = self.message['message']
        power = float(response.split(' ')[-1])
        return power

    def setPower(self, power_in_mw):
        """
        power_in_mw - The desired laser power in mW.
        """
        # print("Setting Power", power_in_mw, self.message)
        if power_in_mw > self.pmax:
            power_in_mw = self.pmax
        self.message = lumencor_httpcommand(command ='SET CHINT '+self.laser_id+' '+ str(int(power_in_mw)), ip=self.ip)
        if self.message['message'][0]=='A':
            return True
        return False

    def shutDown(self):
        """
        Turn the laser off.
        """
        if self.live:
            self.setPower(0)
            self.setLaserOnOff(False)

    def getStatus(self):
        """
        Get the status
        """
        return self.live
   




# if (__name__ == "__main__"):
#     import time
#     obj = LumencorLaser(laser_id=0,ip = '192.168.201.200')
#     if obj.getStatus():
#         print(obj.getPowerRange())
#         print(obj.getLaserOnOff())
#         obj.setLaserOnOff(True)
#         obj.setPower(20.0)
#         time.sleep(0.1)
#         obj.shutDown()


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

#SET calibration or acquisition mode
Calib = True
Acq = False



print ('Calibration [C] or Acquisition [A] mode ?')
mode = input()
if mode == 'Calibration' or mode == 'C' or mode == 'c' :
    Calib = True
    Acq = False

if mode == 'Acquisition'or mode == 'A' or mode == 'a' :
    Acq = True
    Calib = False



#100ms ON - 100ms OFF & 20mW
if Acq == True :
    print ('Laser color 1 ? VIOLET = 0, BLUE = 1, CYAN = 2, TEAL = 3, GREEN = 4, RED = 5 or NIR = 6 ')
    laser_ch1 = int(input())
    laser_color1 = LumencorLaser(laser_id=laser_ch1,ip = '192.168.201.200')
    print ('Power laser 1 ? (mW) ')
    power1 = int(input())
    laser_color1.setPower(power1)

    print ('Laser color 2 ? VIOLET = 0, BLUE = 1, CYAN = 2, TEAL = 3, GREEN = 4, RED = 5 or NIR = 6 ')
    laser_ch2 = int(input())
    laser_color2 = LumencorLaser(laser_id=laser_ch2,ip = '192.168.201.200')
    print ('Power laser 2 ? (mW) ')
    power2 = int(input())
    laser_color2.setPower(power2)
    
    while Acq :
        
        import time
        laser_color1.setLaserOnOff(True)
        time.sleep(0.100)
        laser_color1.setLaserOnOff(False)
        laser_color2.setLaserOnOff(True)
        time.sleep(0.100)
        laser_color2.setLaserOnOff(False)
        if KeyboardInterrupt :
            laser_color1.shutDown()
            laser_color2.shutDown()
            break

#Continuous laser
if Calib == True :
    print ('Laser color ? VIOLET = 0, BLUE = 1, CYAN = 2, TEAL = 3, GREEN = 4, RED = 5 or NIR = 6 ')
    laser_ch = int(input())
    laser_color = LumencorLaser(laser_id=laser_ch,ip = '192.168.201.200')
    print ('Power laser ? (mW) ')
    power = int(input())
    laser_color.setPower(power)

    while Calib :
        laser_color.setLaserOnOff(True)
        if KeyboardInterrupt :
            laser_color.shutDown()
            break
