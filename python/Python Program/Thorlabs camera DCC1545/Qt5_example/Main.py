from os import system
import sys

from PyQt5 import QtWidgets as qtw

from First_Project.View.main_window import Ui_MainWindow
from First_Project import config_parameters, main_path
from First_Project.Model.Experiment.daq_experiment import DAQExperiment
from First_Project.Model.Camera_Thorlabs.camera_thorlabs import CameraThorlabs

class Main():

    def __init__(self):
        """MainWindow constructor.

        This widget will be the main window. All the connections will be defined
        from here.
        """
        super().__init__()
        
        # Open the main window
        # --------------------
        
        self.m = Ui_MainWindow(main_path) # Instentiation of the class Ui_MainWindow()
        
        # Instantiate the classes associated to each instrument
        # -----------------------------------------------------

        self.thor_cam = CameraThorlabs(0) # Instantiation of the class
        
        # Definition of the signal/slot connections for the Thorlabs camera
        # -----------------------------------------------------------------

        self.m.init_cam.connect(self.thor_cam.open_connection)
        self.m.close_cam.connect(self.thor_cam.close_connection)
        self.thor_cam.cam_initialized.connect(self.m.CamID_Edit.setText)
        self.m.start_cam.connect(self.thor_cam.init_acquisition)
        self.thor_cam.cam_acquiring.connect(self.m.Cam_image.setPixmap)
        # self.model.error.connect(self.view.show_error)


if __name__ == '__main__':
    
    system('clear')
    app = qtw.QApplication(sys.argv)

    mw = Main()
    sys.exit(app.exec())