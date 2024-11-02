import shutil
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QGroupBox, QGridLayout, QLineEdit, QSpinBox, QSizePolicy, QFileDialog, QMessageBox
)

import os

from Load_Image.load_image import Load_Image
from Corner_Detection.find_corners import Find_Corners
from Corner_Detection.find_instrinstic import Find_instrintic
from Corner_Detection.find_extrinsic import Find_Extrinsic

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.load_image = Load_Image()
        self.find_corners = Find_Corners()
        self.find_instrintic = Find_instrintic()
        self.find_extrinsic = Find_Extrinsic()

        self.Q3_folder = os.path.join(os.getcwd(), "Q3_image")
        self.imL_path = os.path.join(os.getcwd(), "Q3_image/imL.png")
        self.imR_path = os.path.join(os.getcwd(), "Q3_image/imR.png")
        self.img1_path = os.path.join(os.getcwd(), "Q4_image/img1.png")
        self.img2_path = os.path.join(os.getcwd(), "Q4_image/img2.png")
        self.extrinsic_value = 1

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
        load_button.clicked.connect(lambda: self.load_image.load_folder(self))
        layout.addWidget(load_button)

        load_imgL_btn = QPushButton("Load Image_L")
        load_imgL_btn.clicked.connect(lambda: self.load_and_save_image(self.imL_path))
        layout.addWidget(load_imgL_btn)

        load_imgR_btn = QPushButton("Load Image_R")
        load_imgR_btn.clicked.connect(lambda: self.load_and_save_image(self.imR_path))
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
        layout.addWidget(text_input)
        layout.addWidget(QPushButton("2.1 show words on board"))
        layout.addWidget(QPushButton("2.2 show words vertical"))

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
        load_img1_btn.clicked.connect(lambda: self.load_and_save_image(self.img1_path))
        layout.addWidget(load_img1_btn)

        load_img2_btn = QPushButton("Load Image2")
        load_img2_btn.clicked.connect(lambda: self.load_and_save_image(self.img2_path))
        layout.addWidget(load_img2_btn)


        keypoints_btn = QPushButton("4.1 Keypoints")
        keypoints_btn.clicked.connect(lambda: sift_detect_keypoint(self.img1_path))
        layout.addWidget(keypoints_btn)

        matched_keypoints_btn = QPushButton("4.2 Matched Keypoints")
        matched_keypoints_btn.clicked.connect(lambda: sift_match_keypoint(self.img1_path, self.img2_path))
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
        self.find_instrintic.find_intrinsic(self, self.find_corners.get_object_points_list(),
                                            self.find_corners.get_corners_list(), self.find_corners.get_image_shape())
        # if self.intrinsic_matrix is not None and self.distortion is not None:
        #     print("Intrinsic matrix and distortion coefficients calculated successfully.")
        # else:
        #     print("Failed to calculate intrinsic matrix and distortion coefficients.")

    def handle_find_corner(self):
        """处理查找角点的逻辑"""
        self.find_corners.find_corners(self, self.load_image.get_load_images_folder())

    def handle_find_extrinsic(self):
        """根据用户选择的索引，显示对应的外参矩阵"""
        self.find_extrinsic.find_extrinsic(self, self.find_instrintic.get_rvec(), self.find_instrintic.get_tvec(), self.extrinsic_value)

    def handle_find_distortion(self):
        """计算并显示畸变矩阵"""
        find_distortion_matrix(self.Q1_folder)
    
    def handle_show_result(self):
        """处理显示取消畸变结果的逻辑"""
        if hasattr(self, 'intrinsic_matrix') and hasattr(self, 'distortion'):
            show_undistorted_result(self.Q1_folder, self.intrinsic_matrix, self.distortion)
        else:
            print("Please calculate intrinsic matrix and distortion coefficients first.")


    def load_and_save_image(self, save_path):
        """选择图像并保存到指定路径"""
        try:
            # 创建目标文件夹（如果不存在）
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # 打开文件选择对话框
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp)")
            if file_path:
                # 复制文件到指定路径
                print(f"Copying {file_path} to {save_path}")
                shutil.copy(file_path, save_path)

                # 显示成功信息
                QMessageBox.information(self, "Success", f"Saved image to {save_path}!")
            else:
                QMessageBox.warning(self, "Warning", "No image selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image:\n{str(e)}")



    def handle_stereo_disparity(self):
        """计算并显示 Stereo Disparity Map"""
        if self.imL_path and self.imR_path:
            print(f"Computing Disparity Map for: \nLeft Image: {self.imL_path}\nRight Image: {self.imR_path}")
            compute_stereo_disparity_map(self.imL_path, self.imR_path)
        else:
            print("Please select both left and right images.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
