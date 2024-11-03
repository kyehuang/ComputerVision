from src.Load_Image.load_image import Load_Image
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox
)
import cv2

class SIFT_Keypoints:
    def __init__(self, parent_widget: QWidget):
        self.Load_Image = Load_Image()
        self.parent_widget = parent_widget
        self._load_image_1 = None
        self._load_image_2 = None


    def load_image_1(self):
        self._load_image_1 = self.Load_Image.load_image(self.parent_widget)

    def load_image_2(self):
        self._load_image_2 = self.Load_Image.load_image(self.parent_widget)
    
    def show_sift_detect_keypoint_on_image_1(self):
        self.show_sift_detect_keypoint(self._load_image_1, "image1")
    
    def show_sift_detect_keypoint(self, input_image, image_name):
        if input_image is None:
            QMessageBox.warning(self.parent_widget, "Warning", f"Please load {image_name} first.")
            return 
        image = cv2.imread(input_image)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self.calculate_sift_detect_keypoint(gray_image)

        result_image = cv2.drawKeypoints(gray_image, keypoints, None, color=(0, 255, 0))
        
        try:
            cv2.imshow("Project Letter on Chessboard", result_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            print(e)

    def calculate_sift_detect_keypoint(self, gray_image):
        try:
            sift = cv2.SIFT.create()

            keypoints, descriptors = sift.detectAndCompute(gray_image, None)
            return keypoints, descriptors
        except Exception as e:
            print(e)
            return None, None

    def show_match_keypoint(self):
        if self._load_image_1 is None or self._load_image_2 is None:
            QMessageBox.warning(self.parent_widget, "Warning", "Please load image first.")
            return 
        
        image_1 = cv2.imread(self._load_image_1)
        image_2 = cv2.imread(self._load_image_2)

        gray_image_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
        gray_image_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)
        match_image = self.calculate_matched_keypoint(gray_image_1, gray_image_2, 2)

        # Display the image using OpenCV
        try:
            cv2.imshow("Matched Keypoints", match_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            print(e)
        

    def calculate_matched_keypoint(self, gray_image_1, gray_image_2, k):
        try:
            keypoints_1, descriptors_1 = self.calculate_sift_detect_keypoint(gray_image_1)
            keypoints_2, descriptors_2 = self.calculate_sift_detect_keypoint(gray_image_2)

            matches = cv2.BFMatcher().knnMatch(descriptors_1, descriptors_2, k=k)

            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append([m])  # `cv2.drawMatchesKnn` expects a list of lists

            # Draw matches
            match_image = cv2.drawMatchesKnn(
                gray_image_1, keypoints_1, gray_image_2, keypoints_2, good_matches,
                None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
            )

            return match_image  # Optionally return the image if needed
        except Exception as e:
            print(f"Error: {e}")
            return None
        