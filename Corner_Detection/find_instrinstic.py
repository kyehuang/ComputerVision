import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox, QDialog, QTextEdit
)
import cv2

class Find_instrintic:
    def __init__(self):
        pass

    def find_intrinsic(self, parent_widget:QWidget, object_points_list:np.ndarray, corners_list:np.ndarray, image_shape:tuple):
        if object_points_list is None or corners_list is None or image_shape is None:
            QMessageBox.warning(parent_widget, "Warning", "No object points list, corners list or image shape.\n"
                               + "Please load the images and find the corners first.")
            return
        
        ret, ins, dist, rvec, tvec = cv2.calibrateCamera(object_points_list, corners_list, image_shape,
                                                     None, None)
        if ret:
            self.__show_intrinsic_matrix_window(ins)
            # QMessageBox.information(parent_widget, "Instrintic Matrix", "Intrinsic matrix(Camera matrix)\n" + str(ins))

    def __show_intrinsic_matrix_window(self, intrinsic_matrix:np.ndarray):
        dialog = QDialog()
        dialog.setWindowTitle("Intrinsic Matrix")
        dialog.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        text = QTextEdit()
        text.setPlainText("Instrinsix matrix (camera matrix):\n" + str(intrinsic_matrix))
        layout.addWidget(text)

        dialog.setLayout(layout)
        dialog.exec_()