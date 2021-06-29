import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QApplication, QTableWidgetItem, QFileDialog

from interfaces.widget_camera_addition import Ui_AdditionalCameraSettings
from interfaces.widget_camera_basic import Ui_BasicCameraSettings
from interfaces.widget_light_control import Ui_LightControl
from widget_buttons import Ui_Form as Ui_ButtonsFrame
from widget_video import Ui_VideoFrame


class CameraHolder(QObject):
    def __init__(self,
                 resolution=(640, 480),
                 iso=100,
                 brightness=50,
                 contrast=0,
                 awb_mode='auto',
                 awb_gains=(1.0, 1.0),
                 is_calibrate=False,
                 ):
        super().__init__()
        # self.camera = PiCamera()
        # self.camera.resolution = resolution
        # self.camera.iso = iso
        # self.camera.brightness = brightness
        # self.camera.contrast = contrast
        # self.camera.awb_mode = awb_mode
        # self.camera.awb_gains = awb_gains
        # self.gain_r, self.gain_b = awb_gains
        # self.value = 0
        if is_calibrate:
            pass

    def start(self) -> None:
        pass

    def stop_showing(self) -> None:
        """
        Stop PiCamera() Preview
        """

    def get_calibration(self) -> tuple:
        """
        Get result of calibration with method from QCombobox
        :return: tuple(gain_r, gain_b)
        """
        pass

    def change_brightness(self, current_brightness: int) -> None:
        """
        Set brightness according to current QSlider positions
        """

        pass

    def change_contrast(self, current_contrast: int) -> None:
        """
        Set contrast according to current QSlider position
        """

        pass

    def change_iso(self, current_iso: int) -> None:
        """
        Set iso according to current QSlider position
        """
        pass

    def change_resolution(self, current_resolution: tuple) -> None:
        """
        Set resolution according to current QComboBox position
        """
        pass

    def change_shutter_speed(self, current_shutter_speed: int) -> None:
        """
        Set shutters speed according to current QSlider position
        """
        pass

    def change_awb_mode(self, current_awb_mode: str) -> None:
        """
        Set automatic white balance (awb) according to current QComboBox position
        """
        pass

    def change_calibration_method(self, current_calibration_method) -> None:
        """
        Set custom calibration method according to current QComboBox position
        """
        pass

    def change_gain_r(self, value: float) -> None:
        """
        Set gain_r according to current QSlider position
        """
        pass

    def change_gain_b(self, value: float) -> None:
        """
        Set gain_b according to current QSlider position
        """

        pass

    def set_awb_gains(self) -> None:
        """
        Set both, gain_r and gain_b as a sensitivity of a camera
        """
        self.camera.awb_gains(self.gain_r, self.gain_b)
        pass


class MyWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('RPi Controller')
        self.setGeometry(200, 100, 1600, 600)

        self.main_widget = QWidget()

        self.buttons_widget = QWidget()
        self.additional_camera_setting = QWidget()
        self.basic_camera_setting = QWidget()
        self.light_control_setting = QWidget()
        self.video_stream_widget = QWidget()

        # add button_widget
        self.button_widget = Ui_ButtonsFrame()
        self.button_widget.setupUi(self.buttons_widget)
        # add additional_camera_setting_widget
        self.addi_camera = Ui_AdditionalCameraSettings()
        self.addi_camera.setupUi(self.additional_camera_setting)
        # add basic_camera_setting_widget
        self.basic_camera = Ui_BasicCameraSettings()
        self.basic_camera.setupUi(self.basic_camera_setting)
        # add light_control_widget
        self.light_control = Ui_LightControl()
        self.light_control.setupUi(self.light_control_setting)
        # add video_stream_widget
        self.video = Ui_VideoFrame()
        self.video.setupUi(self.video_stream_widget)
        self.addition_text = ['aaa', 'bbb', 'ccc']
        self.values = {'resolution': self.addi_camera.resolutionComboBox.currentText(),
                       'wb mode': self.addi_camera.wbComboBox.currentText(),
                       'exposure mode': self.addi_camera.ExposureComboBox.currentText(),
                       'brightness': self.basic_camera.brightnessValueLabel.text(),
                       'contrast': self.basic_camera.contrastValueLabel.text(),
                       'iso': self.basic_camera.isoValueLabel.text(),
                       'shutter speed': self.basic_camera.ssValueLabel.text(),
                       'gain_r': float(self.basic_camera.RValueLabel.text()),
                       'gain_b': float(self.basic_camera.BValueLabel.text()),
                       'gains ( r, b )': f'({self.basic_camera.RValueLabel.text(), self.basic_camera.BValueLabel.text()})',
                       }
        self.addi_camera.tableWidget.setFont(QFont('Impact', 8))
        self.addi_camera.wbComboBox.setFont(QFont('Impact', 8))
        self.addi_camera.ExposureComboBox.setFont(QFont('Impact', 8))
        self.addi_camera.resolutionComboBox.setFont(QFont('Impact', 8))
        for row in range(8):
            self.addi_camera.tableWidget.setRowHeight(row, 18)
            self.addi_camera.tableWidget.item(row, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.fill_table(row)

        self.main_layout = QVBoxLayout()
        self.video_layout = QHBoxLayout()
        self.setting_layout = QVBoxLayout()

        self.light_layout = QHBoxLayout()
        self.light_layout.addWidget(self.light_control_setting, 2)
        self.light_layout.addWidget(self.basic_camera_setting, 5)

        self.setting_layout.addLayout(self.light_layout)
        self.setting_layout.addWidget(self.additional_camera_setting)

        self.video_layout.addLayout(self.setting_layout, 4)
        self.video_layout.addWidget(self.video_stream_widget, 7)

        self.main_layout.addLayout(self.video_layout, 7)
        self.main_layout.addWidget(self.buttons_widget, 1)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.addi_camera.wbComboBox.setCurrentIndex(0)
        self.__create_camera_loop()
        self.__setup_sliders()
        self.__setup_combobox()
        self.basic_camera.BSlider.setValue()

        name = QFileDialog.getSaveFileName(self, "Open Image", filter="Image Files (*.png *.jpg *.bmp)", )

    def __setup_sliders(self) -> None:
        """
        Set Reaction onChange for each QSlider on MainWindow
        """
        self.basic_camera.RSlider.valueChanged.connect(self.__change_gain_r)
        self.basic_camera.BSlider.valueChanged.connect(self.__change_gain_b)
        self.basic_camera.isoSlider.valueChanged.connect(self.__change_iso)
        self.basic_camera.brightnessSlider.valueChanged.connect(self.__change_brightness)
        self.basic_camera.contrastSlider.valueChanged.connect(self.__change_contrast)
        self.basic_camera.ssSlider.valueChanged.connect(self.__change_shutter_speed)

    def __setup_combobox(self) -> None:
        """
        Set Reaction onChange for each QComboBox on MainWindow
         """
        self.addi_camera.wbComboBox.currentTextChanged.connect(self.__change_wb_method)
        self.addi_camera.ExposureComboBox.currentTextChanged.connect(self.__change_exposure_mode)
        self.addi_camera.resolutionComboBox.currentTextChanged.connect(self.__change_resolution)

    def fill_table(self, row):
        current_item = self.addi_camera.tableWidget.item(row, 0).text().lower()
        if current_item != 'gains ( r, b )':
            item = QTableWidgetItem(
                self.values[current_item]) if current_item in self.values.keys() else QTableWidgetItem(
                'None')
        else:
            item_str = f"{self.values['gain_r']}, {self.values['gain_b']}"
            item = QTableWidgetItem(item_str)
        self.addi_camera.tableWidget.setItem(row, 1, item)
        self.addi_camera.tableWidget.item(row, 1).setTextAlignment(QtCore.Qt.AlignCenter)

    def __set_gains(self):
        self.values[
            'gains ( r, b )'] = f'({self.basic_camera.RValueLabel.text(), self.basic_camera.BValueLabel.text()})'
        self.fill_table(row=7)

    def __change_wb_method(self, method: str) -> None:
        """
        Set self.values['wb mode'] and fill QTableWidget()
        :param method:
        :return:
        """
        self.values['wb mode'] = method
        self.fill_table(row=5)

    def __change_exposure_mode(self, mode: str) -> None:
        """
        Set self.values['exposure mode'] and fill QTableWidget()
        :param mode:
        :return:
        """
        self.values['exposure mode'] = mode
        self.fill_table(row=6)

    def __change_resolution(self, resolution: str) -> None:
        """
        Set self.values['resolution'] and fill QTableWidget()
        :param resolution:
        :return:
        """
        w, h = resolution.split('x')
        self.values['resolution'] = resolution
        self.fill_table(row=0)

    def __change_gain_r(self, value: int) -> None:
        """
        Set self.values['gain_r'] and fill QTableWidget()
        :param value:
        :return:
        """
        v = value / 100
        self.basic_camera.RValueLabel.setNum(v)
        self.values['gain_b'] = str(v)
        self.__set_gains()
        self.camera.change_gain_r(value=v)

    def __change_gain_b(self, value: int) -> None:
        """
        Set self.values['gain_b'] and fill QTableWidget()
        :param value:
        :return:
        """
        v = value / 100
        self.basic_camera.BValueLabel.setNum(v)
        self.values['gain_r'] = str(v)
        self.__set_gains()
        self.camera.change_gain_b(value=v)

    def __change_iso(self, value: int) -> None:
        """
        Set self.values['iso'] and fill QTableWidget()
        :param value:
        :return:
        """
        self.basic_camera.isoValueLabel.setNum(value)
        self.values['iso'] = str(value)
        self.fill_table(row=3)
        self.camera.change_iso(value)

    def __change_contrast(self, value: int) -> None:
        """
        Set self.values['contrast'] and fill QTableWidget()
        :param value:
        :return:
        """
        self.basic_camera.contrastValueLabel.setNum(value)
        self.values['contrast'] = str(value)
        self.fill_table(row=2)
        self.camera.change_contrast(value)

    def __change_brightness(self, value: int) -> None:
        """
        Set self.values['brightness'] and fill QTableWidget()
        :param value:
        :return:
        """
        self.basic_camera.brightnessValueLabel.setNum(value)
        self.values['brightness'] = str(value)
        self.fill_table(row=1)
        self.camera.change_brightness(value)

    def __change_shutter_speed(self, value: int) -> None:
        """
        Set self.values['shutter speed'] and fill QTableWidget()
        :param value:
        :return:
        """
        self.basic_camera.ssValueLabel.setNum(value)
        self.values['shutter speed'] = str(value)
        self.fill_table(row=4)
        self.camera.change_shutter_speed(value)

    def __create_camera_loop(self) -> None:
        """
        Create QThread() for PiCamera() Preview
        """
        self.thread = QThread(self)
        self.camera = CameraHolder()
        self.camera.moveToThread(self.thread)
        self.thread.started.connect(self.camera.start)
        self.thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
