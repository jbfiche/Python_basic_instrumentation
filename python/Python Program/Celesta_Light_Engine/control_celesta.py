#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:21:43 2020

@author: marion
using the work of Bogdan Bintu
"""
import sys
import urllib.request
import traceback
import time

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
        try:
            # See if the system returns back the right IP.
            self.message = self.getIP()
            # assert (self.message['message'] == 'A IP '+self.ip)
            # assert (int(self.laser_id)<self.getNumberLasers())
            self.live = True
        except:
            # print(traceback.format_exc())
            self.live = False
            # print("Failed to connect to Lumencor Laser at ip:", self.ip)

        if self.live:
            [self.pmin, self.pmax] = self.getPowerRange()
            self.setExtControl(True)
            if (not self.getLaserOnOff()):
                self.setLaserOnOff(False)

                
# WORK IN PROGRESS
#    def getNumberLasers(self):
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
        

class Laser_control :
    """
    Controlling lasers with predefined sequences
    """
    
    def __init__(self, color1, color2, power, power2, expo_time) :
        
        if color1 in range(0,6) :
            self.color1 = color1
            self.power = power
            self.expo_time = expo_time
            self.laser1 = LumencorLaser(laser_id = self.color1, ip = '192.168.201.200')
            
        else :
            print('There is an error in your command, please choose a color for L1 between 0 and 6 \n\nFor your information : VIOLET = 0, BLUE = 1, CYAN = 2, TEAL = 3, GREEN = 4, RED = 5 or NIR = 6')
            sys.exit()
        
        if color2 in range(0,6) :
            print('You are using two colors')
            self.color2 = color2
            self.power2 = power2
            self.laser2 = LumencorLaser(laser_id = self.color2, ip = '192.168.201.200')
        elif color2 == None :
            print('You are using only one color')
        else :
            print('There is an error in your command, please choose a color for L2 between 0 and 6 \n\nFor your information : VIOLET = 0, BLUE = 1, CYAN = 2, TEAL = 3, GREEN = 4, RED = 5 or NIR = 6')
            sys.exit()

    
    def one_color_calib(self) :
        """
        Continuous illumination for calibration
        """
        self.laser1.setPower(self.power)
        self.laser1.setLaserOnOff(True)        
    
    def one_color_acq(self) :
        """
        Sequential illumination for monocolor acquisitions
        
        Sequence to control one laser
        100 ms ON - 100 ms OFF
        """
        self.laser1.setPower(self.power)
        self.laser1.setLaserOnOff(True)
        time.sleep(self.expo_time)
        self.laser1.setLaserOnOff(False)
        time.sleep(self.expo_time)

    def two_colors_acq(self):
        """
        Sequential illumination for multicolor acquisitions
        
        Sequence to control two lasers
        100 ms ON Laser 1 - 100 ms OFF Laser 1 - 100 ms ON Laser 2 - 100 ms OFF Laser 2
        """
        self.laser1.setPower(self.power)
        self.laser2.setPower(self.power2)
        self.laser1.setLaserOnOff(True)
        time.sleep(self.expo_time)
        self.laser1.setLaserOnOff(False)
        time.sleep(self.expo_time)
        self.laser2.setLaserOnOff(True)
        time.sleep(self.expo_time)
        self.laser2.setLaserOnOff(False)
        time.sleep(self.expo_time)
    
    def turn_off_L1(self) :
        self.laser1.setLaserOnOff(False)
    
    def turn_off_L2(self) :
        self.laser2.setLaserOnOff(False)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

#SET calibration or acquisition mode
Calib = False
Acq = True


# Are you using one or two lasers ?
# For one laser, num_laser = 1
# For two lasers, num_laser = 2
num_laser = 2

#Exposure time of the camera ? (s)
expo_time_cam = 0.100

#Laser color 1 ? VIOLET = 0, BLUE = 1, CYAN = 2, TEAL = 3, GREEN = 4, RED = 5 or NIR = 6
first_color = 0

# Power laser 1 ? (mW)
laser_power_1 = 20.0

#Laser color 2 ? VIOLET = 0, BLUE = 1, CYAN = 2, TEAL = 3, GREEN = 4, RED = 5 or NIR = 6
second_color = 5

# Power laser 2 ? (mW)
laser_power_2 = 20.0

#Laser control for one color 
#There is no modification to do here
LC1 = Laser_control(color1=first_color,power=laser_power_1,expo_time=expo_time_cam,color2=None,power2=None)

#Laser control for one color
#There is no modification to do here
LC2 = Laser_control(color1 = first_color,color2 = second_color,power=laser_power_1,power2=laser_power_2,expo_time=expo_time_cam,)

#100ms ON - 100ms OFF
if Acq == True :
    print('Acquisition running ...')
    while Acq :
        if num_laser == 1 :
            try :
                LC1.one_color_acq()
            except KeyboardInterrupt :
                LC1.turn_off_L1()
                print("End of acquisition - Laser off")
                sys.exit()
        elif num_laser == 2 :
            try :
                LC2.two_colors_acq()
            except KeyboardInterrupt :
                LC2.turn_off_L1()
                LC2.turn_off_L2()
                print("End of acquisition - All lasers off")
                sys.exit() 
        else :
            print("There is an error in the number of lasers you are asking for")
            sys.exit()

#Continuous laser
if Calib == True :
    print('Calibration running ...')
    while Calib :
        try :
            LC1.one_color_calib()
        except KeyboardInterrupt :
            LC1.turn_off_L1()
            print("End of calibration - Laser off")
            sys.exit()









#
# The MIT License
#
# Copyright (c) 2013 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
