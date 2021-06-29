import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon

from .WIDGET_Addition_setting import AdditionCameraSettings
from .WIDGET_Basic_setting import BasicCameraSettings
from .WIDGET_Buttons import ButtonsWidget
from .WIDGET_light_settings import LightController
from .WIDGET_video import VideoHolder
from .camera_module import CameraHolder


class MyWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('RPi-Camera Controller')
        self.setWindowIcon(QIcon('/home/pi/Desktop/RPiCameraApp_newest_v/source/icons/raspberry-pi.png'))
        self.showMaximized()
        self.setup_ui()
        self.connect_basic_slider_and_table()
        self.__create_camera_loop()
        self.__send_initial_data_to_table()
        self.connect_additional_combobox_and_camera()

    def connect_additional_combobox_and_camera(self):
        self.camera_additional.ui.wbComboBox.currentTextChanged.connect(self.get_awb_on_change)
        self.camera_additional.ui.ExposureComboBox.currentTextChanged.connect(self.get_exposure_on_change)
        self.camera_additional.ui.resolutionComboBox.currentTextChanged.connect(self.get_resolution_on_change)

    def connect_basic_slider_and_table(self):
        self.camera_basic.ui.contrastSlider.valueChanged.connect(self.get_contrast_on_change)
        self.camera_basic.ui.brightnessSlider.valueChanged.connect(self.get_br_on_change)
        self.camera_basic.ui.isoSlider.valueChanged.connect(self.get_iso_on_change)
        self.camera_basic.ui.RSlider.valueChanged.connect(self.get_gain_r_on_change)
        self.camera_basic.ui.BSlider.valueChanged.connect(self.get_gain_b_on_change)
        self.camera_basic.ui.ssSlider.valueChanged.connect(self.get_ss_on_change)

    def get_resolution_on_change(self, value):
        w, h = value.split('x')
        self.camera.change_resolution((int(w), int(h)))

    def get_awb_on_change(self, value):
        self.camera.change_awb_mode(value)

    def get_exposure_on_change(self, value):
        self.camera.change_exposure_mode(value)

    def get_iso_on_change(self, value):
        self.camera_additional.set_iso(str(value))
        self.camera.change_iso(value)

    def get_br_on_change(self, value):
        self.camera_additional.set_brightness(str(value))
        self.camera.change_brightness(value)

    def get_contrast_on_change(self, value):
        self.camera_additional.set_contrast(str(value))
        self.camera.change_contrast(value)

    def get_ss_on_change(self, value):
        self.camera_additional.set_shutter_speed(str(value))
        self.camera.change_shutter_speed(value)

    def get_gain_r_on_change(self, value):
        gain_b = self.camera_basic.ui.BValueLabel.text()
        self.camera_additional.set_gains(f'{str(value / 100)}    {gain_b}')
        self.camera.change_gain_r(value / 100)

    def get_gain_b_on_change(self, value):
        gain_r = self.camera_basic.ui.RValueLabel.text()
        self.camera_additional.set_gains(f'{gain_r}    {str(value / 100)}')
        self.camera.change_gain_b(value / 100)

    def setup_ui(self):
        self.ui = QWidget()
        self.light_control = LightController()
        self.camera_basic = BasicCameraSettings()
        self.camera_additional = AdditionCameraSettings()
        self.video_frame = VideoHolder()
        self.buttons = ButtonsWidget(self)
        self.firstLayout = QHBoxLayout()
        self.firstLayout.addWidget(self.light_control, 2)
        self.firstLayout.addWidget(self.camera_basic, 3)
        self.secondLayour = QVBoxLayout()
        self.secondLayour.addLayout(self.firstLayout)
        self.secondLayour.addWidget(self.camera_additional)
        self.thirdLayout = QHBoxLayout()
        self.thirdLayout.addLayout(self.secondLayour, 3)
        self.thirdLayout.addWidget(self.video_frame, 6)
        self.fourthLayout = QVBoxLayout()
        self.fourthLayout.addLayout(self.thirdLayout, 7)
        self.fourthLayout.addWidget(self.buttons, 1)
        self.ui.setLayout(self.fourthLayout)
        self.setCentralWidget(self.ui)
        
    def set_slider_brightness(self,value):
        self.camera_basic.set_slider_brightness(value)
    
    def set_slider_contrast(self,value):
        self.camera_basic.set_slider_contrast(value)
    
    def set_slider_iso(self,value):
        self.camera_basic.set_slider_iso(value)
    
    def set_slider_shutter_speed(self,value):
        self.camera_basic.set_slider_shutter_speed(value)
    
    def set_slider_gain_r(self,value):
        self.camera_basic.set_slider_gain_r(value)
    
    def set_slider_gain_b(self,value):
        self.camera_basic.set_slider_gain_b(value)
    
    def __create_camera_loop(self) -> None:
        """
        Create QThread() for PiCamera() Preview
        """
        self.thread = QThread(self)
        self.camera = CameraHolder(parent=self,
                                   brightness=self.camera_basic.get_current_brightness(),
                                   contrast=self.camera_basic.get_current_contrast(),
                                   iso=self.camera_basic.get_current_iso(),
                                   awb_gains=(
                                       self.camera_basic.get_current_gain_r(), self.camera_basic.get_current_gain_b()),
                                   awb_mode=self.camera_additional.get_current_wb_mode(),
                                   resolution=self.camera_additional.get_current_resolution(),
                                   shutter_speed=self.camera_basic.get_current_shutter_speed(),
                                   exposure_mode=self.camera_additional.get_current_exposure_mode()
                                   )
        self.camera.moveToThread(self.thread)
        self.thread.started.connect(self.camera.start)
        self.thread.start()

    def __send_initial_data_to_table(self):
        self.get_iso_on_change(100)
        self.get_br_on_change(50)
        self.get_contrast_on_change(0)
        self.get_gain_r_on_change(110)
        self.get_ss_on_change(12000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
