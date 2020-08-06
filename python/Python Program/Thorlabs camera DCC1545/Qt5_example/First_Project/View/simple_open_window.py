#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:48:33 2020

@author: fiche
"""


import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'GUI/main_window.ui'), self)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = QMainWindow()
    
    m.show()
    app.exit(app.exec_())
    print('done')
