import cv2
import numpy as np
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox
)

class Find_Corners:
    def __init__(self,):
        self.chessboard_size = (11, 8)
        self.winSize = (11, 11)
        self.zeroZone = (-1, -1)
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.square_size = 0.02

        self.object_points_list = []
        self.corners_list = []
        self.image_shape = None
        pass

    def find_corners(self, parent_widget:QWidget, _load_images_folder:str):
        """
        Find the chess board corners

        Parameters:
            parent_widget: QWidget
                The parent widget to display the dialog
            _load_images_folder: str
                The folder path of the images to be loaded
        """
        # Get the folder path of the images to be loaded
        if _load_images_folder is None:
            QMessageBox.warning(parent_widget, "Warning", "No folder selected.")
            return
        images = self.__get_image_from_folder(_load_images_folder)
        
        # Get the images from the folder path
        if images is None:
            QMessageBox.warning(parent_widget, "Warning", "Failed to load images.")
            return
        
        # Find the chess board corners
        for image in images:
            self.image_shape = image.shape[:2]
            image_with_corners, corners = self.__find_corner(image)
            if image_with_corners is not None:
                cv2.imshow("Chess Board Corners", image_with_corners)
                cv2.waitKey(0)
                self.object_points_list.append(self.__init_object_points())
                self.corners_list.append(corners)
            else:
                QMessageBox.warning(parent_widget, "Warning", "Failed to find the chess board corners.")
                return
        cv2.destroyAllWindows()
    
    def get_object_points_list(self):
        """
        Get the object points list

        Returns:
            np.ndarray: The object points list
        """
        return self.object_points_list

    def get_corners_list(self):
        """
        Get the corners list

        Returns:
            np.ndarray: The corners list
        """
        return self.corners_list

    def get_image_shape(self):
        """
        Get the image shape

        Returns:
            tuple: The image shape
        """
        return self.image_shape

    def __find_corner(self, image):
        """
        Find the chess board corners

        Parameters:
            image: np.ndarray
                The image

        Returns:
            np.ndarray: The image with the chess board corners
            np.ndarray: The corners
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        ret, corners = cv2.findChessboardCorners(gray, self.chessboard_size, None)
        if ret:
            corners = cv2.cornerSubPix(gray, corners, self.winSize, self.zeroZone, self.criteria)
            cv2.drawChessboardCorners(image, self.chessboard_size, corners, ret)
            return image, corners
        else:
            return None, None
        
    def __get_image_from_folder(self, folder_path):
        """
        Get the image from the folder path

        Parameters:
            folder_path: str
                The folder path of the image

        Returns:
            np.ndarray: The image
        """
        try:
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.bmp', '.jpg', '.jpeg', '.png'))]
            image_files.sort(key=lambda x: int(os.path.splitext(x)[0]))
            if not image_files:
                raise ValueError("No valid image files found in the selected folder.")
            
            images = []
            for image_file in image_files:
                image_path = os.path.join(folder_path, image_file)
                image = cv2.imread(image_path)
                if image is None:
                    raise ValueError(f"Failed to read image from {image_path}")
                images.append(image)
            return images
        except Exception as e:
            raise e
            print(e)
            return None

    def __init_object_points(self):
        """
        Initialize the object points

        Returns:
            np.ndarray: The object points
        """
        object_points = np.zeros((np.prod(self.chessboard_size), 3), np.float32)
        object_points[:, :2] = np.indices(self.chessboard_size).T.reshape(-1, 2)
        object_points *= self.square_size
        return object_points