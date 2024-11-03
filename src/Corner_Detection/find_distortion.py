import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog, QVBoxLayout, QTextEdit

class Find_Distortion:
    def __init__(self):
        pass

    def find_distortion(self, parent_widget:QWidget, find_intrinsic_obj):
        if find_intrinsic_obj is None:
            QMessageBox.warning(parent_widget, "Warning", "No intrinsic matrix found.\n"
                                + "Please find the intrinsic matrix first.")
            return
        
        distortion = find_intrinsic_obj.get_distortion_coefficients()
        if distortion is None:
            QMessageBox.warning(parent_widget, "Warning", "No distortion coefficients found.\n"
                                + "Please find the intrinsic matrix first.")
            return
        
        self.__show_distortion_matrix_window(distortion)
    
    def __show_distortion_matrix_window(self, distortion:np.ndarray):
        dialog = QDialog()
        dialog.setWindowTitle("Distortion Coefficients")
        dialog.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        text = QTextEdit()
        text.setPlainText("Distortion coefficients:\n" + str(distortion))
        layout.addWidget(text)

        dialog.setLayout(layout)
        dialog.exec_()