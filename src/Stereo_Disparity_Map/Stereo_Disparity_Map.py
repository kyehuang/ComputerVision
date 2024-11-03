from src.Load_Image.load_image import Load_Image
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox, QDialog, QTextEdit
)
from PyQt5.QtGui import QPixmap, QImage

import cv2
import numpy as np

class Stereo_Disparity_Map:
    def __init__(self, numDisparities: int = 432, blockSize: int = 25):
        self.Load_Image = Load_Image()
        self.numDisparities = numDisparities
        self.blockSize = blockSize
        pass

    def load_imageL(self,parent_widget: QWidget):
        self.Load_Image.load_imageL(parent_widget)

    def load_imageR(self,parent_widget: QWidget):
        self.Load_Image.load_imageR(parent_widget)

    def compute_stereo_disparity_map(self, parent_widget: QWidget):
        stereo = cv2.StereoBM.create(numDisparities=self.numDisparities, blockSize=self.blockSize)
        imageL_path, imageR_path = self.Load_Image.get_load_imageLandR()

        if imageL_path is None or imageR_path is None:
            QMessageBox.warning(parent_widget, "Warning", "No image loaded.")
            return None, None, None
        
        imageL = cv2.imread(imageL_path)
        imageR = cv2.imread(imageR_path)

        disparity = stereo.compute(cv2.cvtColor(imageL, cv2.COLOR_BGR2GRAY), cv2.cvtColor(imageR, cv2.COLOR_BGR2GRAY))

        # Normalize the disparity map for visualization
        disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        disparity_normalized = np.uint8(disparity_normalized)

        self.disparity = disparity_normalized  # Store the normalized result if needed

        
        return disparity_normalized, imageL, imageR
    
    def show_stereo_disparity_map_window(self, parent_widget: QWidget):

        disparity, imageL, imageR = self.compute_stereo_disparity_map(parent_widget)
        if disparity is None:
            return

        self.__show_window(parent_widget, imageL, "ImageL", 0, 100)
        self.__show_window(parent_widget, imageR, "ImageR", 425, 100)
        self.__show_window(parent_widget, disparity, "Disparity", 900, 100)
    
    def __show_window(self, parent_widget: QWidget, image, title, x, y):
        dialog = QDialog(parent_widget)
        dialog.setWindowTitle(title)
        dialog.resize(400, 400)
        dialog.move(x, y)
        layout = QHBoxLayout()
        label = QLabel()
        disparity_resized = cv2.resize(image, (400, 400))
        pixmap = QPixmap.fromImage(self.cv2_to_qt(disparity_resized))
        label.setPixmap(pixmap)
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.show()

    def cv2_to_qt(self, cv_image):
        """将 OpenCV 图像转换为 QImage"""
        if len(cv_image.shape) == 3:  # Color image (height, width, channels)
            height, width, channel = cv_image.shape
            bytes_per_line = channel * width
            return QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        elif len(cv_image.shape) == 2:  # Grayscale image (height, width)
            height, width = cv_image.shape
            bytes_per_line = width
            return QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        else:
            raise ValueError("Invalid image shape for conversion")