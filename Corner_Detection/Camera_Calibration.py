from Corner_Detection.find_corners import Find_Corners
from Corner_Detection.find_instrinstic import Find_instrintic
from Corner_Detection.find_extrinsic import Find_Extrinsic
from Corner_Detection.find_distortion import Find_Distortion
from Corner_Detection.show_result import Show_Result
from Load_Image.load_image import Load_Image

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox, QDialog, QTextEdit
)

class Camera_Calibration:
    def __init__(self):
        # Initialize the classes
        self.Find_Corners = Find_Corners()
        self.Find_instrintic = Find_instrintic()
        self.Find_Extrinsic = Find_Extrinsic()
        self.Find_Distortion = Find_Distortion()
        self.Show_Result = Show_Result()
        self.Load_Image = Load_Image()

    def load_folder(self, parent_widget):
        self.Load_Image.load_folder(parent_widget)
        self.Find_Corners.find_corners_without_window(self.Load_Image.get_load_images_folder())
        self.Find_instrintic.find_intrinsic_with_window(self.Find_Corners.get_object_points_list(),
                                                        self.Find_Corners.get_corners_list(), self.Find_Corners.get_image_shape())

    def find_corners(self, parent_widget):
        self.Find_Corners.find_corners(parent_widget, self.Load_Image.get_load_images_folder())
    
    def find_intrinsic(self, parent_widget):
        self.Find_instrintic.find_intrinsic(parent_widget, self.Find_Corners.get_object_points_list(), 
                                    self.Find_Corners.get_corners_list(), self.Find_Corners.get_image_shape())
        
    def find_extrinsic(self, parent_widget, index):
        self.Find_Extrinsic.find_extrinsic(parent_widget, self.Find_instrintic.get_rvec(), 
                                           self.Find_instrintic.get_tvec(), index)
        
    def find_distortion(self, parent_widget):
        self.Find_Distortion.find_distortion(parent_widget, self.Find_instrintic)

    def show_result(self, parent_widget, index):        
        self.Show_Result.show_result(parent_widget, self.Find_Corners.get_image(index), 
                                     self.Find_instrintic.get_intrinsic_matrix(), 
                                     self.Find_instrintic.get_distortion_coefficients(), 
                                     )
        
    def get_image_information(self, parent_widget, index):
        if self.Find_instrintic.get_intrinsic_matrix() is None:
            QMessageBox.warning(parent_widget, "Warning", "No object points list, corners list.\n"
                               + "Please load the images and find the corners first.")
            return

        image_information = self.Find_Corners.get_image(index), self.Find_instrintic.get_intrinsic_matrix(), self.Find_instrintic.get_distortion_coefficients(), self.Find_instrintic.get_rvec()[index], self.Find_instrintic.get_tvec()[index]
        return image_information

    def get_all_images(self):
        return self.Find_Corners.get_all_images().copy()