from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox
)
import os

class Load_Image:
    """
    class to store the folder path of the images to be loaded
    """
    def __init__(self):
        self._load_images_folder = None

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
    
