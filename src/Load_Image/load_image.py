from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox
)
import os
import copy
class Load_Image:
    """
    class to store the folder path of the images to be loaded
    """
    def __init__(self):
        self._load_images_folder = None
        self._load_imageL = None
        self._load_imageR = None

    def load_folder(self, parent_widget: QWidget):
        """
        Get the folder path of the images to be loaded

        Parameters:
            parent_widget: QWidget
                The parent widget to display the dialog
        """
        try:
            folder_path = QFileDialog.getExistingDirectory(parent_widget, 'Select Folder')
            if folder_path:
                valid_extensions = ('.bmp', '.jpg', '.jpeg', '.png')
                image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]

                if not image_files:
                    QMessageBox.warning(parent_widget, "Warning", "No valid image files found in the selected folder.")
                    return
                
                self._load_images_folder = folder_path
                QMessageBox.information(parent_widget, "Success", f"Loaded {len(image_files)} images from {folder_path}!")
            
            else:
                QMessageBox.warning(parent_widget, "Warning", "No folder selected.")
        except Exception as e:
            QMessageBox.critical(parent_widget, "Error", f"Failed to load images:\n{str(e)}")
            print(e)
    
    def get_load_images_folder(self):
        """
        Get the folder path of the images to be loaded

        Returns:
            str: The folder path of the images to be loaded
        """
        if self._load_images_folder is None:
            return None
        
        return self._load_images_folder

    def load_image(self, parent_widget: QWidget):
        """
        Load an image from the file dialog

        Parameters:
            parent_widget: QWidget
                The parent widget to display the dialog

        Returns:
            str: The file path of the loaded image
        """
        try:
            file_path, _ = QFileDialog.getOpenFileName(parent_widget, "Select Image", "", "Images (*.png *.jpg *.bmp)")
            if file_path:
                QMessageBox.information(parent_widget, "Success", f"Loaded image from {file_path}!")
                return file_path
            else:
                QMessageBox.warning(parent_widget, "Warning", "No image selected.")
                return None
        except Exception as e:
            QMessageBox.critical(parent_widget, "Error", f"Failed to load image:\n{str(e)}")
            print(e)

        return None

    def load_imageL(self, parent_widget: QWidget):
        """
        Load the left image from the file dialog

        Parameters:
            parent_widget: QWidget
                The parent widget to display the dialog

        Returns:
            str: The file path of the loaded left image
        """
        self._load_imageL = self.load_image(parent_widget)
        return self._load_imageL

    def load_imageR(self, parent_widget: QWidget):
        """
        Load the right image from the file dialog

        Parameters:
            parent_widget: QWidget
                The parent widget to display the dialog

        Returns:
            str: The file path of the loaded right image
        """
        self._load_imageR = self.load_image(parent_widget)
        return self._load_imageR

    def get_load_imageLandR(self):
        """
        Get the file paths of the loaded left and right images

        Returns:
            tuple: A tuple containing the file paths of the loaded left and right images
        """
        return copy.deepcopy(self._load_imageL), copy.deepcopy(self._load_imageR)