import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

from .interfaces.widget_camera_basic import Ui_BasicCameraSettings


class BasicCameraSettings(QWidget):
    """
    Widget for holding main camera settings such as:
        Brightness
        Contrast
        ISO
        Gain R
        Gain B
        Shutter Speed
    if table => Set all of values to the table else => set it just to QLabel near sliders
    """

    def __init__(self, table=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_BasicCameraSettings()
        self.ui.setupUi(self)
        self.table = table
        self.__setup_sliders()

    def __setup_sliders(self):
        self.ui.RSlider.valueChanged.connect(self.__set_gain_r)
        self.ui.BSlider.valueChanged.connect(self.__set_gain_b)
        self.ui.isoSlider.valueChanged.connect(self.set_iso)
        self.ui.contrastSlider.valueChanged.connect(self.set_contrast)
        self.ui.brightnessSlider.valueChanged.connect(self.set_brightness)
        self.ui.ssSlider.valueChanged.connect(self.set_shutter_speed)

        self.ui.RSlider.setValue(110)
        self.ui.BSlider.setValue(95)
        self.ui.isoSlider.setValue(100)

    def set_brightness(self, value: str):
        """
        Set Brightness Value to the valueLabal
        :param value: string
        :return:
        """
        self.ui.brightnessValueLabel.setText(str(value))

    def set_contrast(self, value: str):
        """
        Set Brightness Value to the valueLabal
        :param value: string
        :return:
        """
        self.ui.contrastValueLabel.setText(str(value))

    def set_iso(self, value: str):
        """
        Set Brightness Value to the valueLabal
        :param value: string
        :return:
        """
        self.ui.isoValueLabel.setText(str(value))

    def set_shutter_speed(self, value: str):
        """
        Set Brightness Value to the valueLabal
        :param value: string
        :return:
        """
        self.ui.ssValueLabel.setText(str(value))

    def set_gain_r(self, r_gain: int):
        """
        Set gain_r Value to the valueLabel
        :param value: string
        :return:
        """
        self.ui.RValueLabel.setText(r_gain)

    def __set_gain_r(self, value: int):
        """
        Process the value from QSlider and send it to the next function
        :param value: int
        :return:
        """
        v = value / 100
        self.set_gain_r(str(v))

    def set_gain_b(self, b_gain: str):
        """
        Set gain_r Value to the valueLabel
        :param value: string
        :return:
        """
        self.ui.BValueLabel.setText(b_gain)

    def __set_gain_b(self, value: int):
        """
        Process the value from QSlider and send it to the next function
        :param value: int
        :return:
        """
        v = value / 100
        self.set_gain_b(str(v))

    def get_current_brightness(self):
        """
        :return: int
        """
        return self.ui.brightnessSlider.value()

    def get_current_contrast(self):
        """
        :return: int
        """
        return self.ui.contrastSlider.value()

    def get_current_iso(self):
        """
        :return: int
        """
        return self.ui.isoSlider.value()

    def get_current_gain_r(self):
        """
        :return: float
        """
        return self.ui.RSlider.value() / 100

    def get_current_gain_b(self):
        """
        :return: float
        """
        return self.ui.RSlider.value() / 100

    def get_current_shutter_speed(self):
        """
        :return: int
        """
        return self.ui.ssSlider.value()
    
    def set_slider_brightness(self,value):
        self.ui.brightnessSlider.setValue(value)
        
    def set_slider_contrast(self,value):
        self.ui.contrastSlider.setValue(value)
    
    def set_slider_iso(self,value):
        self.ui.isoSlider.setValue(value)
    
    def set_slider_shutter_speed(self,value):
        self.ui.ssSlider.setValue(value)
    
    def set_slider_gain_r(self,value):
        v = int(value*100)
        self.ui.RSlider.setValue(v)
        
    
    def set_slider_gain_b(self,value):
        v = int(value*100)
        self.ui.BSlider.setValue(v)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BasicCameraSettings()
    window.show()
    sys.exit(app.exec())
