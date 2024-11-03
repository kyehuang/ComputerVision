import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox, QDialog, QTextEdit
)

from Corner_Detection.Camera_Calibration import Camera_Calibration

class Show_Words_On_Chessboard:
    def __init__(self, alphabet_db_onboard_path=None, offset=None):
        """
        alphabet_db_onboard_path: str
            Path to the file containing the alphabet database
        offset: np.ndarray
            Offset to be added to the alphabet database
        """
        self.alphabet_db_onboard_path = alphabet_db_onboard_path
        self.fs = cv2.FileStorage(self.alphabet_db_onboard_path, cv2.FILE_STORAGE_READ)
        if not self.fs.isOpened():
            raise FileNotFoundError(f"Unable to open file at {self.alphabet_db_onboard_path}")
        
        self.offset = offset
        pass

    def show_words_on_chessboard(self, parent_widget:QWidget, text, Camera_Calibration:Camera_Calibration):
        if len(text) > 6:
            QMessageBox.warning(parent_widget, "Warning", "length of text must less than 6")
            return 
        
        text = text.upper()          
        all_images = Camera_Calibration.get_all_images()

        for image_index in range(len(all_images)):
            NewCharPoints_list = self.__calculate_NewCharPoints_list(text, parent_widget, image_index, Camera_Calibration)
            
            self.__draw_line(NewCharPoints_list, all_images[image_index])
            cv2.imshow("Project Letter on Chessboard", all_images[image_index])
            cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __calculate_NewCharPoints_list(self, text, parent_widget, image_index, Camera_Calibration):
        NewCharPoints_list = []
        for index in range(len(text)):
            charPoints = self.fs.getNode(text[index]).mat()
            _ , ins, dist, rvec, tvec = Camera_Calibration.get_image_information(parent_widget, image_index)
            charPoints += self.offset[index]
            
            # Convert to appropriate type and reshape if needed
            if charPoints is not None:
                charPoints = np.array(charPoints, dtype=np.float32).reshape(-1, 3)
                if charPoints.ndim == 2:
                    charPoints = charPoints.reshape(-1, 1, 3) 
            NewCharPoints, _ = cv2.projectPoints(charPoints, rvec, tvec, ins, dist)
            NewCharPoints_list.append(NewCharPoints)
        return NewCharPoints_list
    
    def __draw_line(self, NewCharPoints_list, image):
        for NewCharPoints in NewCharPoints_list:
            for i in range(0, len(NewCharPoints) - 1, 2):
                if i + 1 < len(NewCharPoints):
                    x1, y1 = int(NewCharPoints[i][0][0]), int(NewCharPoints[i][0][1])
                    x2, y2 = int(NewCharPoints[i + 1][0][0]), int(NewCharPoints[i + 1][0][1])
                    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 15)