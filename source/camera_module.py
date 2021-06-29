import time
from picamera import PiCamera

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox 

from .Calibrator_correct import PiCameraCalibrator

class CameraHolder(QObject):

    def __init__(self,
                 parent,
                 resolution=(640, 480),
                 iso=100,
                 brightness=50,
                 contrast=0,
                 awb_gains=(1.0, 1.0),
                 shutter_speed=12000,
                 exposure_mode='auto',
                 awb_mode='auto',
                 ):
        super().__init__()
        self.parent = parent
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.iso = iso
        self.camera.brightness = brightness
        self.camera.contrast = contrast
        self.camera.awb_mode = awb_mode
        self.camera.awb_gains = awb_gains
        self.gain_r, self.gain_b = awb_gains
        calibrator = PiCameraCalibrator(my_camera=self.camera,
                                             gain_r = self.gain_r,
                                             gain_b = self.gain_b)
        self.calibration_methods = {'gray world':calibrator.gray_world,
                                    'retinex':calibrator.retinex,
                                    'standard deviation':calibrator.std,
                                    'white patches':calibrator.white_patches}

    def start(self) -> None:
        self.camera.start_preview(fullscreen=False,window=(800,150,920,720))

    def stop_showing(self) -> None:
        """
        Stop PiCamera() Preview
        """

    def get_calibration(self, mode):
        """
        Get result of calibration with method from QCombobox
        :return: tuple(gain_r, gain_b)
        """
        calibrator = PiCameraCalibrator(my_camera=self.camera,
                                             gain_r = self.gain_r,
                                             gain_b = self.gain_b)
        try:
            respond = mode()
        except (ValueError,NameError,IndexError) as error:
            print('Error', error)
            msg = QMessageBox()
            msg.setText(f"An Error '{error}' Occure during\ncalibration with {mode} method");
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec()
        else:            
            self.gain_r, self.gain_b = self.camera.awb_gains
            br = self.camera.brightness
            contr = self.camera.contrast
            self.parent.set_slider_brightness(br)
            self.parent.set_slider_contrast(contr)
            self.parent.set_slider_gain_r(self.gain_r)
            self.parent.set_slider_gain_b(self.gain_b)
        
    def get_siquence(self):
        name = QFileDialog.getSaveFileName(caption='Open Image', filter="Image Files (*.png *.jpg *.bmp *)")
        res = self.parent.camera_additional.get_current_resolution()
        br = self.parent.camera_basic.get_current_brightness()
        iso = self.parent.camera_basic.get_current_iso()
        ss = self.parent.camera_basic.get_current_shutter_speed()
        method = self.parent.camera_additional.get_current_wb_mode()
        self.image_default_name = f'{name[0]}_{res}_{br}_{iso}_{ss}'
        print([self.image_default_name])
        for i in range(len(self.formats)):
            self.set_pixmap('red')
            self.parent.camera.camera.capture(self.image_default_name,format=self.formats[i])
            self.set_pixmap('green')
        
        

    def change_brightness(self, current_brightness: int) -> None:
        """
        Set brightness according to current QSlider positions
        """

        self.camera.brightness = current_brightness

    def change_contrast(self, current_contrast: int) -> None:
        """
        Set contrast according to current QSlider position
        """
        self.camera.contrast = current_contrast

    def change_iso(self, current_iso: int) -> None:
        """
        Set iso according to current QSlider position
        """
        self.camera.iso = current_iso

    def change_resolution(self, current_resolution: tuple) -> None:
        """
        Set resolution according to current QComboBox position
        """
        self.camera.resolution = current_resolution

    def change_shutter_speed(self, current_shutter_speed: int) -> None:
        """
        Set shutters speed according to current QSlider position
        """
        self.camera.shutter_speed = current_shutter_speed

    def change_awb_mode(self, current_awb_mode: str) -> None:
        """
        Set automatic white balance (awb) according to current QComboBox position
        """
        if current_awb_mode:
            if current_awb_mode not in self.calibration_methods:
                self.camera.awb_mode = current_awb_mode
                self.gain_r,self.gain_b = self.camera.awb_gains
                self.parent.set_slider_gain_r(self.gain_r)
                self.parent.set_slider_gain_b(self.gain_b)                
            else:
                self.get_calibration(mode = self.calibration_methods[current_awb_mode])
                
            
    def change_exposure_mode(self, current_exposure_mode: str) -> None:
        """
        Set automatic white balance (awb) according to current QComboBox position
        """
        self.camera.exposure_mode = current_exposure_mode

    def change_gain_r(self, value: float) -> None:
        """
        Set gain_r according to current QSlider position
        """
        self.gain_r = value
        self.set_awb_gains()

    def change_gain_b(self, value: float) -> None:
        """
        Set gain_b according to current QSlider position
        """

        self.gain_b = value
        self.set_awb_gains()

    def set_awb_gains(self) -> None:
        """
        Set both, gain_r and gain_b as a sensitivity of a camera
        """
        self.camera.awb_gains=(self.gain_r, self.gain_b)
        pass
