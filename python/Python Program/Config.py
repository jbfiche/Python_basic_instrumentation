#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 09:58:40 2020

@author: aymerick 
"""

'''
Config for "Wells 60"
'''
NbWellsWidth=5      # Number of Wells in Width (Axis Y of the printer)
NbWellsLength=16    # Number of Wells in Length (Axis X of the printer)
DifferenceW=13      # Differemce between the center of 2 Wells in Width (Unit : mm)(AxisY)
DifferenceL=13      # Difference between the center of 2 Wells in Length (Unit : mm)(AxisX)

'''
Config for the printer 3d-mill
'''
PortPrinter='/dev/ttyUSB1'      # Communication port of the printer

'''
Config for the valve Hamilton serial MVP
'''
NbofValve=1                                                                     # Nb of valve in series
PortValve='/dev/ttyS0'                                                          # Communication port of the first valve 
ValveNB=("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p")       # List wich contains all the adress possible 
ValveConfigPosition={};
ValveConfigPosition["a"]=8                                                      # Configuration of the first valve 
ValveConfigPosition["b"]=2                                                      # Configuration of the seconde valve
ValveConfigPosition["c"]=2                                                      # .... You can add new ConfigPosition if you use more than 3 valve

'''
Config for the Ms-2000
'''
PortMS2000='COM4'            # Communication port of the MS2000
LED=False                    # True if there is a LED
ZAxis=False                  # True if the device can moove in z axis

'''
Config PY Controller
'''
PYName='C-663'
PYID='0105500035'
NbofAxes=1