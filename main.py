import shutil
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox
)
import os

from Corner_Detection.Camera_Calibration import Camera_Calibration
from Augmented_Reailty.Augmented_Reailty import Augmented_Reailty
from Stereo_Disparity_Map.Stereo_Disparity_Map import Stereo_Disparity_Map
from SIFT_Keypoints.SIFT_Keypoints import SIFT_Keypoints

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.Camera_Calibration = Camera_Calibration()
        self.Augmented_Reailty = Augmented_Reailty()
        self.Stereo_Disparity_Map = Stereo_Disparity_Map()
        self.SIFT_Keypoints = SIFT_Keypoints(self)

        self.Q3_folder = os.path.join(os.getcwd(), "Q3_image")
        self.imL_path = os.path.join(os.getcwd(), "Q3_image/imL.png")
        self.imR_path = os.path.join(os.getcwd(), "Q3_image/imR.png")
        self.img1_path = os.path.join(os.getcwd(), "Q4_image/img1.png")
        self.img2_path = os.path.join(os.getcwd(), "Q4_image/img2.png")
        self.extrinsic_value = 1
        self.text_input = ""

        # 设置窗口标题和大小
        self.setWindowTitle('MainWindow - cvdlhw1.ui')
        self.setGeometry(100, 100, 800, 600)

        # 创建主布局（水平布局）
        main_layout = QHBoxLayout()

        # 创建子布局和分组框
        main_layout.addWidget(self.create_load_image_group())
        main_layout.addWidget(self.create_calibration_group())
        main_layout.addWidget(self.create_augmented_reality_group())
        main_layout.addWidget(self.create_stereo_disparity_group())
        main_layout.addWidget(self.create_sift_group())

        # 设置主窗口的布局
        self.setLayout(main_layout)

    def create_load_image_group(self):
        """加载图片的分组框"""
        group = QGroupBox("Load Image")
        layout = QVBoxLayout()

        load_button = QPushButton("Load folder")
        load_button.clicked.connect(lambda: self.Camera_Calibration.load_folder(self))
        layout.addWidget(load_button)

        load_imgL_btn = QPushButton("Load Image_L")
        load_imgL_btn.clicked.connect(lambda: self.Stereo_Disparity_Map.load_imageL(self))
        layout.addWidget(load_imgL_btn)

        load_imgR_btn = QPushButton("Load Image_R")
        load_imgR_btn.clicked.connect(lambda: self.Stereo_Disparity_Map.load_imageR(self))
        layout.addWidget(load_imgR_btn)

        group.setLayout(layout)
        return group

    def create_calibration_group(self):
        """校准功能的分组框"""
        group = QGroupBox("1. Calibration")
        layout = QVBoxLayout()  # 使用垂直布局排列组件

        # 添加按钮和 QSpinBox 到布局中
        find_corners_btn = QPushButton("1.1 Find corners")
        find_corners_btn.clicked.connect(lambda: (self.handle_find_corner()))
        layout.addWidget(find_corners_btn)

        find_intrinsic_btn = QPushButton("1.2 Find intrinsic")
        find_intrinsic_btn.clicked.connect(self.handle_find_intrinsic)
        layout.addWidget(find_intrinsic_btn)

        group_extrinsic = self.create_extrinsic_group()
        group_extrinsic.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(group_extrinsic)


        find_distortion_btn = QPushButton("1.4 Find Distortion")
        find_distortion_btn.clicked.connect(self.handle_find_distortion)
        layout.addWidget(find_distortion_btn)

        show_result_btn = QPushButton("1.5 Show Result")
        show_result_btn.clicked.connect(self.handle_show_result)
        layout.addWidget(show_result_btn)

        # 设置分组框的布局
        group.setLayout(layout)
        return group

    def create_extrinsic_group(self):
        """外参矩阵的分组框"""
        group = QGroupBox("1.3 Find Extrinsic")
        layout = QVBoxLayout()

        spin_box = QSpinBox()
        spin_box.setRange(1, 15)
        spin_box.setValue(1)
        spin_box.valueChanged.connect(self.handle_spin_value_change)
        layout.addWidget(spin_box)


        find_extrinsic_btn = QPushButton("1.3 Find Extrinsic")
        find_extrinsic_btn.clicked.connect(self.handle_find_extrinsic)
        # find_extrinsic_btn.setFixedHeight(50)
        layout.addWidget(find_extrinsic_btn)

        group.setLayout(layout)
        return group

    def create_augmented_reality_group(self):
        """增强现实功能的分组框"""
        group = QGroupBox("2. Augmented Reality")
        layout = QVBoxLayout()

        text_input = QLineEdit()
        text_input.setPlaceholderText("Type Here")  # 占位符
        text_input.textChanged.connect(lambda: self.handle_text_input_change(text_input.text()))
        layout.addWidget(text_input)

        show_words_on_board_btn = QPushButton("2.1 show words on board")
        show_words_on_board_btn.clicked.connect(lambda: self.handle_show_words_on_board())
        layout.addWidget(show_words_on_board_btn)

        show_words_on_board_btn = QPushButton("2.2 show words vertical")
        show_words_on_board_btn.clicked.connect(lambda: self.handle_show_words_vertical())
        layout.addWidget(show_words_on_board_btn)

        group.setLayout(layout)
        return group

    def create_stereo_disparity_group(self):
        """立体视差的分组框"""
        group = QGroupBox("3. Stereo disparity map")
        layout = QVBoxLayout()

        compute_disparity_btn = QPushButton("3.1 Stereo Disparity Map")
        compute_disparity_btn.clicked.connect(self.handle_stereo_disparity)
        layout.addWidget(compute_disparity_btn)

        group.setLayout(layout)
        return group

    def create_sift_group(self):
        """SIFT 特征检测的分组框"""
        group = QGroupBox("4. SIFT")
        layout = QVBoxLayout()

        load_img1_btn = QPushButton("Load Image1")
        load_img1_btn.clicked.connect(lambda: self.SIFT_Keypoints.load_image_1())
        layout.addWidget(load_img1_btn)

        load_img2_btn = QPushButton("Load Image2")
        load_img2_btn.clicked.connect(lambda: self.SIFT_Keypoints.load_image_2())
        layout.addWidget(load_img2_btn)


        keypoints_btn = QPushButton("4.1 Keypoints")
        keypoints_btn.clicked.connect(lambda: self.SIFT_Keypoints.show_sift_detect_keypoint_on_image_1())
        layout.addWidget(keypoints_btn)

        matched_keypoints_btn = QPushButton("4.2 Matched Keypoints")
        matched_keypoints_btn.clicked.connect(lambda: self.SIFT_Keypoints.show_match_keypoint())
        layout.addWidget(matched_keypoints_btn)

        group.setLayout(layout)
        return group
    
    def handle_load_folder(self, target_folder):
        """处理加载文件夹按钮的点击事件"""
        load_and_save_images(self, target_folder)

    def handle_spin_value_change(self, value):
        """当 SpinBox 的值发生变化时更新存储的值"""
        self.extrinsic_value = value

    def print_spin_value(self):
        """打印当前存储的 SpinBox 的值"""
        print(f"Current SpinBox Value: {self.extrinsic_value}")


    def handle_find_intrinsic(self):
        """计算并存储内参和畸变矩阵"""
        self.Camera_Calibration.find_intrinsic(self)
        # if self.intrinsic_matrix is not None and self.distortion is not None:
        #     print("Intrinsic matrix and distortion coefficients calculated successfully.")
        # else:
        #     print("Failed to calculate intrinsic matrix and distortion coefficients.")

    def handle_find_corner(self):
        """处理查找角点的逻辑"""
        self.Camera_Calibration.find_corners(self)

    def handle_find_extrinsic(self):
        """根据用户选择的索引，显示对应的外参矩阵"""
        self.Camera_Calibration.find_extrinsic(self, self.extrinsic_value)
    def handle_find_distortion(self):
        """计算并显示畸变矩阵"""
        self.Camera_Calibration.find_distortion(self)
    
    def handle_show_result(self):
        """处理显示取消畸变结果的逻辑"""
        if 1 > self.extrinsic_value or self.extrinsic_value > 15:
            QMessageBox.warning(self, "Warning", "Please select a valid index.")
            return

        
        self.Camera_Calibration.show_result(self, self.extrinsic_value)

    def handle_text_input_change(self, text):
        """处理文本输入框的文本变化"""
        self.text_input = text

    def handle_show_words_on_board(self):
        self.Augmented_Reailty.show_words_on_board(self, self.text_input, self.Camera_Calibration)

    def handle_show_words_vertical(self):
        self.Augmented_Reailty.show_words_vertical(self, self.text_input, self.Camera_Calibration)




    def handle_stereo_disparity(self):
        """计算并显示 Stereo Disparity Map"""
        self.Stereo_Disparity_Map.show_stereo_disparity_map_window(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
