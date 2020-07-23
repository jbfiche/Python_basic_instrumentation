#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 09:58:40 2020

@author: aymerick 48 7
"""

'''
Config for "Wells 60"
'''
NbWellsWidth=5      #Number of Wells in Width (Axis Y of the printer)
NbWellsLength=16    #Number of Wells in Length (Axis X of the printer)
DifferenceW=13      #Differemce between the center of 2 Wells in Width (Unit : mm)(AxisY)
DifferenceL=13      #Difference between the center of 2 Wells in Length (Unit : mm)(AxisX)
XWell_1=53          #Coordinates of the starting Well
YWell_1=10
ZWell_1=30

'''
Config for the printer
'''
PortPrinter='/dev/ttyUSB0'  #Port of communication of the printer

'''
Config for the valve
'''
NbofValve=3
PortValve='COM1'
ValveNB=("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p")
ValveConfigPosition={};
ValveConfigPosition["a"]=8
ValveConfigPosition["b"]=2
ValveConfigPosition["c"]=2

