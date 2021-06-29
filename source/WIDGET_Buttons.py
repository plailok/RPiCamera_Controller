import sys
from datetime import datetime

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog

import RPi.GPIO as gpio
from .interfaces.widget_buttons import Ui_Form as Ui_Buttons
    

class ButtonsWidget(QWidget):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Buttons()
        self.ui.setupUi(self)
        self.parent = parent
        self.image_name_default = str()
        self.video_name_default = str()

        self.image_save_signal = pyqtSignal
        self.exit_signal = pyqtSignal
        self.set_default_signal = pyqtSignal
        self.__setup_buttons()
        self.ui.stopButton.setEnabled(False)
        self.set_pixmap('green')
        
        self.formats = ['.jpeg', '.png', '.bmp']

    def __setup_buttons(self):
        self.ui.captureButton.pressed.connect(self.__capture_button_pressed)
        self.ui.captureseriesButton.pressed.connect(self.__capture_series_button_pressed)
        self.ui.startButton.pressed.connect(self.__start_recording_button_pressed)
        self.ui.stopButton.pressed.connect(self.__stop_recording_button_pressed)
        self.ui.setdefaultButton.pressed.connect(self.__set_default_button_pressed)
        self.ui.exitButton.pressed.connect(self.__exit_button_pressed)

    def set_image_name_default(self, name: str = 'Image') -> None:
        """
        Set name by default for images
        :param name:
        :return:
        """
        self.image_name_default = name
        self.video_name_default = name

    def set_video_name_default(self, name: str = 'Video') -> None:
        """
        Set name by default for video
        :param name:
        :return:
        """
        self.image_name_default = name

    def set_bubble_color(self, color: str = 'white') -> None:
        """
        Set QLabel with a new color according to current state of App:
            green - Ready to Use
            red - Occupied by capturing video
            white - No signal from camer
        Basic Setting is for white
        :param color:
        :return:
        """
        if type(color) is str:
            style = f'background-color:{color}'
            self.ui.indicator.setStyleSheet(style)
        else:
            raise NameError('No such color in the list')

    def save_image(self, name=False):
        if not name:
            name = QFileDialog.getSaveFileName(caption='Open Image', filter="Image Files (*.png *.jpg *.bmp *.tiff)")
        else:
            self.image_save_signal()

    def set_pixmap(self, color: str):
        """
        Set pixmap for indicator
        Acsess color as a parameter:
            green for green aquarium .ico
            red for red aquarium .ico
        :param color:
        """
        if color == 'green':
            self.ui.indicator.setPixmap(QPixmap('/home/pi/Desktop/RPiCameraApp_newest_v/source/icons/green_aquarium.png'))
        elif color == 'red':
            self.ui.indicator.setPixmap(QPixmap('/home/pi/Desktop/RPiCameraApp_newest_v/source/icons/red_aquarium.png'))
        else:
            raise ValueError(f'No such color {color} available')

    def __capture_button_pressed(self):
        self.set_pixmap('red')
        
        name, res, br, iso, ss, method = self.__get_name_and_parameter()
        im_format = '.png'
        image_name = f'{name[0]}_{res}_{br}_{iso}_{ss}_{method}'
        self.parent.camera.camera.capture(image_name + im_format)
        
        self.set_pixmap('green')

    def __capture_series_button_pressed(self):
        self.set_pixmap('red')
        
        name, res, br, iso, ss, method = self.__get_name_and_parameter()
        image_name = f'{name[0]}_{res}_{br}_{iso}_{ss}_{method}'          
        for i in range(len(self.formats)):
            self.parent.camera.camera.capture(image_name+self.formats[i])
            
        self.set_pixmap('green')
        
    def __get_name_and_parameter(self,is_video=False):
        if is_video:
            name = QFileDialog.getSaveFileName(caption='Save Video As', filter="Video Files (*.h264 *.mpeg *.mp4 *)")
        else:
            name = QFileDialog.getSaveFileName(caption='Open Image', filter="Image Files (*.png *.jpg *.bmp *)")
        if not name:
            return
        res = self.parent.camera_additional.get_current_resolution()
        br = self.parent.camera_basic.get_current_brightness()
        iso = self.parent.camera_basic.get_current_iso()
        ss = self.parent.camera_basic.get_current_shutter_speed()
        method = self.parent.camera_additional.get_current_wb_mode()
        if ' ' in method:
            method.replace(' ','_')
        return name,res,br,iso,ss,method
            
    def __start_recording_button_pressed(self):
        try:
            name, res, br, iso, ss, method = self.__get_name_and_parameter(is_video=True)
            self.video_default_name = f'{name[0]}_{res}_{br}_{iso}_{ss}_{method}'
            self.parent.camera.camera.start_recording(self.video_default_name + '.h264')
        except (NameError, ValueError, IndexError, PiCameraError,Exception) as exc:
            self.__add_to_log(exc) 
        else:
            self.ui.stopButton.setEnabled(True)
            self.set_pixmap('red')
            

    def __stop_recording_button_pressed(self):
        try:
            self.parent.camera.camera.stop_recording()
        except (NameError, ValueError, IndexError, PiCameraError, Exception) as exc:
            self.__add_to_log(exc) 
        else:
            self.ui.stopButton.setEnabled(False)
            self.set_pixmap('green')
            
    def __set_default_button_pressed(self):
        self.parent.camera.camera.stop_preview()
        self.parent.set_slider_brightness(50)
        self.parent.set_slider_contrast(0)
        self.parent.set_slider_iso(100)
        self.parent.set_slider_shutter_speed(12000)
        self.parent.set_slider_gain_r(1.1)
        self.parent.set_slider_gain_b(1.05)
        self.parent.camera.change_brightness(50)
        self.parent.camera.change_contrast(0)
        self.parent.camera.change_iso(100)
        self.parent.camera.change_shutter_speed(12000)
        self.parent.camera.change_gain_r(1.1)
        self.parent.camera.change_gain_b(1.05)
        self.parent.camera.change_awb_mode('auto')
        self.parent.camera.change_exposure_mode('off')
        self.parent.camera.change_resolution((1920,1080))
        self.parent.camera.camera.start_preview(fullscreen=False,window=(800,150,920,720))

    def __exit_button_pressed(self):
        try:
            gpio.cleanup()
            self.parent.close()
        except (RuntimeWarning, Exception) as error:
            self.__add_to_log(error)
        
    def __add_to_log(self,to_log:str):
        time = datetime.now()
        with open('Rpi_application_log.log','a+') as log:
            log.write(f"{time}: {to_log} ")
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ButtonsWidget()
    window.show()
    sys.exit(app.exec())
