import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QMessageBox
class Find_Extrinsic:
    def __init__(self):
        pass

    def find_extrinsic(self, parent_widget:QWidget, rvec:np.ndarray, tvec:np.ndarray, extrinsic_index:int):
        if rvec is None or tvec is None:
            QMessageBox.warning(parent_widget, "Warning", "No rvec or tvec.\n"
                               + "Please find the instrinsic matrix first.")
            return
        
        if extrinsic_index <= 0 or extrinsic_index >= len(rvec):
            QMessageBox.warning(parent_widget, "Warning", "Invalid extrinsic index.\n"
                               + "Please select a valid extrinsic index.")
            return
        
        rotation_matrix, _ = cv2.Rodrigues(rvec[extrinsic_index - 1])
        
        extrinsic_matrix = np.hstack((rotation_matrix, tvec[extrinsic_index - 1]))
        QMessageBox.information(parent_widget, "Extrinsic Matrix", f"Extrinsic matrix:\n{extrinsic_matrix}")

        return extrinsic_matrix