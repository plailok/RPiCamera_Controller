import sys
import RPi.GPIO as gpio
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

from .interfaces.widget_light_control import Ui_LightControl


class LightController(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_LightControl()
        self.ui.setupUi(self)
        
        self.red_icon = QIcon('/home/pi/Desktop/RPiCameraApp_newest_v/source/icons/red_lamp.png')
        self.green_icon = QIcon('/home/pi/Desktop/RPiCameraApp_newest_v/source/icons/green_lamp.png')
        self.ui.LightControlFrame.setStyleSheet("QCheckBox::indicator {width: 0px;height: 0px;}")
        self.lights = {'visible 1':[5, gpio.HIGH],
                       'visible 2':[4, gpio.HIGH],
                       'red': [20,21, gpio.HIGH],
                       'ir': [3, 24, gpio.HIGH],
                       'uv':[6, 23, gpio.HIGH]}
        try:
            self.__setup_checkboxes()
            self.__setup_lights()
        except Exception as exc:
            self.ui.self.ui.visibleCBox_1.setEnabled(False)
            self.ui.self.ui.visibleCBox_2.setEnabled(False)
            self.ui.redCBox.setEnabled(False)
            self.ui.infraredCBox.setEnabled(False)
            self.ui.ultravioletCBox.setEnabled(False)
            
            
        
    
    def __setup_lights(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(6,gpio.OUT) #right UV
        gpio.setup(23,gpio.OUT) #left UV
        gpio.setup(18,gpio.OUT) #camera, HIGH=VIS, LOW=IR/UV
        gpio.setup(3,gpio.OUT) #left IR
        gpio.setup(24,gpio.OUT) #right IR
        gpio.setup(20,gpio.OUT) #left Red strip
        gpio.setup(21,gpio.OUT) #right Red strip
        gpio.setup(5,gpio.OUT) #White strip2
        gpio.setup(4,gpio.OUT) #White strip1
        for light, mode in self.lights.items():
            self.__check_light_state(mode)

    def __setup_checkboxes(self):
        self.ui.visibleCBox_1.stateChanged.connect(self._check_visible_1)
        self.ui.visibleCBox_1.setIcon(self.red_icon)
        self.ui.visibleCBox_2.stateChanged.connect(self._check_visible_2)
        self.ui.visibleCBox_2.setIcon(self.red_icon)
        self.ui.redCBox.stateChanged.connect(self._check_red)
        self.ui.redCBox.setIcon(self.red_icon)
        self.ui.infraredCBox.stateChanged.connect(self._check_ir)
        self.ui.infraredCBox.setIcon(self.red_icon)
        self.ui.ultravioletCBox.stateChanged.connect(self._check_uv)
        self.ui.ultravioletCBox.setIcon(self.red_icon)

    def _check_visible_1(self, state):
        if state == 2:
            self.lights['visible 1'][-1] = 0
            self.ui.visibleCBox_1.setIcon(self.green_icon)
        else:
            self.lights['visible 1'][-1] = 1
            self.ui.visibleCBox_1.setIcon(self.red_icon)
        self.__check_light_state(self.lights['visible 1'])

    def _check_visible_2(self, state):
        if state == 2:
            self.lights['visible 2'][-1] = 0
            self.ui.visibleCBox_2.setIcon(self.green_icon)
        else:
            self.lights['visible 2'][-1] = 1
            self.ui.visibleCBox_2.setIcon(self.red_icon)
        self.__check_light_state(self.lights['visible 2'])
        
    def _check_red(self, state):
        if state == 2:
            self.lights['red'][-1] = 0
            self.ui.redCBox.setIcon(self.green_icon)
        else:
            self.lights['red'][-1] = 1
            self.ui.redCBox.setIcon(self.red_icon)
        self.__check_light_state(self.lights['red'])

    def _check_ir(self, state):
        if state == 2:
            self.lights['ir'][-1] = 0
            self.ui.infraredCBox.setIcon(self.green_icon)
        else:
            self.lights['ir'][-1] = 1
            self.ui.infraredCBox.setIcon(self.red_icon)
        self.__check_light_state(self.lights['ir'])

    def _check_uv(self, state):
        if state == 2:
            self.lights['uv'][-1] = 0
            self.ui.ultravioletCBox.setIcon(self.green_icon)
        else:
            self.lights['uv'][-1] = 1
            self.ui.ultravioletCBox.setIcon(self.red_icon)
        self.__check_light_state(self.lights['uv'])
        
    def __check_light_state(self, value) -> None:
        """
        Turn off and tunr on light if changed
        """
        if len(value) != 2:
            lights=[value[:2]]
            current_state = value[2]
            for l in lights:
                gpio.output(l, current_state)
        elif len(value) == 2:
            gpio.output(value[0],value[1])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LightController()
    window.show()
    sys.exit(app.exec())
