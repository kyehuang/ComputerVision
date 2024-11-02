from PyQt5.QtWidgets import QMessageBox
import cv2
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import sys

class Show_Result:
    def show_result(self, parent_widget, image, instrinsic_matrix, distortion_coefficients):
        if image is None:
            QMessageBox.warning(parent_widget, "Warning", "No image found.\n"
                                + "Please load the image first.")
            return
        
        if instrinsic_matrix is None or distortion_coefficients is None:
            QMessageBox.warning(parent_widget, "Warning", "No intrinsic matrix or distortion coefficients found.\n"
                                + "Please calculate intrinsic matrix and distortion coefficients first.")
            return
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        undistorted_image = cv2.undistort(gray, instrinsic_matrix, distortion_coefficients)
        
        self.__show_result_window(parent_widget, gray, undistorted_image)
    
    def __show_result_window(self,parent_widget, original_image, undistorted_image):
        # Create and show dialog for original image
        dialog_original = QDialog(parent_widget)
        dialog_original.setWindowTitle("Original Chessboard")
        dialog_original.resize(400, 400)
        dialog_original.move(100, 100)  # Set position of the original image window
        layout_original = QHBoxLayout()
        original_label = QLabel()
        original_image_resized = cv2.resize(original_image, (400, 400))
        original_pixmap = QPixmap.fromImage(self.cv2_to_qt(original_image_resized))
        original_label.setPixmap(original_pixmap)
        original_label.setAlignment(Qt.AlignCenter)
        layout_original.addWidget(original_label)
        dialog_original.setLayout(layout_original)
        dialog_original.show()
        
        # Create and show dialog for undistorted image
        dialog_undistorted = QDialog(parent_widget)
        dialog_undistorted.setWindowTitle("Undistorted Chessboard")
        dialog_undistorted.resize(400, 400)
        dialog_undistorted.move(600, 100)  # Set position of the undistorted image window
        layout_undistorted = QHBoxLayout()
        undistorted_label = QLabel()
        undistorted_image_resized = cv2.resize(undistorted_image, (400, 400))
        undistorted_pixmap = QPixmap.fromImage(self.cv2_to_qt(undistorted_image_resized))
        undistorted_label.setPixmap(undistorted_pixmap)
        undistorted_label.setAlignment(Qt.AlignCenter)
        layout_undistorted.addWidget(undistorted_label)
        dialog_undistorted.setLayout(layout_undistorted)
        dialog_undistorted.show()
        
   
    def cv2_to_qt(self, cv_image):
        """将 OpenCV 图像转换为 QImage"""
        height, width = cv_image.shape
        bytes_per_line = width
        return QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

