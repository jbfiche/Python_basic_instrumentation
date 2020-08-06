#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:48:33 2020

@author: fiche
"""
from os import path

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic


class Ui_MainWindow(qtw.QMainWindow):
    
    init_cam = qtc.pyqtSignal(int)
    close_cam = qtc.pyqtSignal()
    start_cam = qtc.pyqtSignal()
    
    def __init__(self, main_path):
        super().__init__()

        # Load the GUI 
        # ------------
        
        GUI_path = path.join(main_path, 'View/GUI/main_window.ui')
        uic.loadUi(GUI_path, self) # Load the pre-defined GUI
        self.show()
        
        # Defines the connection
        # ----------------------

        # self.DAQinit_Button.clicked.connect(self.initDAQ)
        # self.DAQstop_Button.clicked.connect(self.releaseDAQ)
        # self.Pump_Button.clicked.connect(self.pump_clicked)
        self.CloseGUI_Button.clicked.connect(self.closeGUI)
        self.InitCam_Button.clicked.connect(self.init_ThorlabsCam)
        self.CloseCam_Button.clicked.connect(self.release_ThorlabsCam)
        self.StartCam_Button.clicked.connect(self.start_acquisition_ThorlabsCam)
          
    # def initDAQ(self):
    #     DAQ_sn = self.config_parameters['DAQ']['serial_number']
    #     daq = DAQExperiment(DAQ_sn)
    #     return daq
        
    # def releaseDAQ(self, daq):
    #     daq.stop()
        
    # def pump_clicked(self):
    #     ao_channel = self.parameter['DAQ']['ao_pump']
    #     flow_rate = self.FlowRate_Edit.text()
    #     volume = self.Volume_Edit.text()
    #     print("The volume to inject is {}µl at {}µl/min".format(volume, flow_rate))
    #     self.daq.pump_injection(float(flow_rate),float(volume),ao_channel)
        
    @qtc.pyqtSlot()
    def init_ThorlabsCam(self):
        
        print('Initializing ...')
        h = self.Camhandle_Edit.text() # Read the handle value from the GUI
        h = int(h)
        if h>=0 and h<255 :
            self.init_cam.emit(h)
        else :
            print('The handle value needs to be between 0 and 254. Initialization is aborted.')
            
            
    @qtc.pyqtSlot()
    def start_acquisition_ThorlabsCam(self):
        self.start_cam.emit()
        
        
    @qtc.pyqtSlot()
    def release_ThorlabsCam(self):
        self.close_cam.emit()
        
    
    @qtc.pyqtSlot()
    def closeGUI(self):
        print("Closing software")
        self.close()
        
