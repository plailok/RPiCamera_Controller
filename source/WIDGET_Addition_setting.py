import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem

from .interfaces.widget_camera_addition import Ui_AdditionalCameraSettings


class AdditionCameraSettings(QWidget):
    """
    Widget for holding additional camera settings such as:
        White Balance Mode
        Exposure Mode
        Resolution
    """

    RPI_BASIC_METHOD = ['off',
                        'auto',
                        'sunlight',
                        'shade',
                        'cloudy',
                        'tungsten',
                        'fluorescent',
                        'incandescent',
                        'flash',
                        'horizon']
    RPI_CUSTOM_METHOD = ['off', 'gray world', 'retinex', 'standard deviation','white patches']
    ALIGNMENT = QtCore.Qt.AlignCenter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_AdditionalCameraSettings()
        self.ui.setupUi(self)
        self.set_resolution(self.ui.resolutionComboBox.currentText())
        self.set_awb_method(self.ui.wbComboBox.currentText())
        self.set_exposure_mode(self.ui.ExposureComboBox.currentText())
        self.__setup_check_box()
        self.__setup_combobox()
        for row in range(8):
            self.ui.tableWidget.setRowHeight(row, 18)
            self.ui.tableWidget.item(row, 0).setTextAlignment(AdditionCameraSettings.ALIGNMENT)

    def __setup_check_box(self):
        self.ui.isCustumCheckBox.stateChanged.connect(self.__check_box_state_changed)

    def __setup_combobox(self):
        self.ui.wbComboBox.currentTextChanged.connect(self.__set_wb)
        self.ui.ExposureComboBox.currentTextChanged.connect(self.__set_exposure)
        self.ui.resolutionComboBox.currentTextChanged.connect(self.__set_resolution)

    def set_resolution(self, resolution):
        """
        Add resolution parameter to table
        :param resolution:
        :return:
        """
        item = QTableWidgetItem(resolution)
        self.ui.tableWidget.setItem(0, 1, item)
        self.ui.tableWidget.item(0, 1).setTextAlignment(AdditionCameraSettings.ALIGNMENT)

    def set_brightness(self, brightness):
        """
        Add brightness parameter to table
        :param brightness:
        :return:
        """
        item = QTableWidgetItem(brightness)
        self.ui.tableWidget.setItem(1, 1, item)
        self.ui.tableWidget.item(1, 1).setTextAlignment(AdditionCameraSettings.ALIGNMENT)

    def set_contrast(self, contrast: str):
        """
        Add contrast parameter to table
        :param contrast:
        :return:
        """
        item = QTableWidgetItem(contrast)
        self.ui.tableWidget.setItem(2, 1, item)
        self.ui.tableWidget.item(2, 1).setTextAlignment(AdditionCameraSettings.ALIGNMENT)

    def set_iso(self, iso: str):
        """
        Add iso parameter to table
        :param iso:
        :return:
        """
        item = QTableWidgetItem(iso)
        self.ui.tableWidget.setItem(3, 1, item)
        self.ui.tableWidget.item(3, 1).setTextAlignment(AdditionCameraSettings.ALIGNMENT)

    def set_shutter_speed(self, shutter_speed: str):
        """
        Add shutter speed parameter to table
        :param shutter_speed:
        :return:
        """
        item = QTableWidgetItem(shutter_speed)
        self.ui.tableWidget.setItem(4, 1, item)
        self.ui.tableWidget.item(4, 1).setTextAlignment(AdditionCameraSettings.ALIGNMENT)

    def set_awb_method(self, awb_method: str):
        """
        Add current white balance method to table
        :param awb_method:
        :return:
        """
        item = QTableWidgetItem(awb_method)
        self.ui.tableWidget.setItem(5, 1, item)
        self.ui.tableWidget.item(5, 1).setTextAlignment(AdditionCameraSettings.ALIGNMENT)

    def set_exposure_mode(self, exposure_mode: str):
        """
        Add current white balance method to table
        :param exposure_mode:
        :return:
        """
        item = QTableWidgetItem(exposure_mode)
        self.ui.tableWidget.setItem(6, 1, item)
        self.ui.tableWidget.item(6, 1).setTextAlignment(AdditionCameraSettings.ALIGNMENT)

    def set_gains(self, gains: str):
        """
        Add current gains of camera to table
        :param gains:
        :return:
        """
        item = QTableWidgetItem(gains)
        self.ui.tableWidget.setItem(7, 1, item)
        self.ui.tableWidget.item(7, 1).setTextAlignment(AdditionCameraSettings.ALIGNMENT)

    def get_current_wb_mode(self) -> str:
        """
        :return: QComboBox.currentText
        """
        return self.ui.wbComboBox.currentText()

    def get_current_exposure_mode(self) -> str:
        """

        :return: QComboBox.currentText -> str
        """
        return self.ui.ExposureComboBox.currentText()

    def get_current_resolution(self) -> str:
        """

        :return: QComboBox.currentText -> str in format (WIDTHxHEIGHT)
         """
        return self.ui.resolutionComboBox.currentText()

    def __check_box_state_changed(self, state):
        if state == 2:
            self.ui.wbComboBox.clear()
            self.ui.wbComboBox.addItems(AdditionCameraSettings.RPI_CUSTOM_METHOD)
        elif state == 0:
            self.ui.wbComboBox.clear()
            self.ui.wbComboBox.addItems(AdditionCameraSettings.RPI_BASIC_METHOD)
        else:
            raise ValueError('CheckBox has only two states')

    def __set_wb(self, method) -> None:
        """
        Reaction on_change event in QComboBox.WhiteBalance currentText
        :param method:
        :return:
        """
        self.set_awb_method(method)

    def __set_exposure(self, mode) -> None:
        """
        Reaction on_change event in QComboBox.ExposureMode currentText
        :param mode:
        :return:
        """
        self.set_exposure_mode(mode)

    def __set_resolution(self, resolution) -> None:
        """
        Reaction on_change event in QComboBox.ExposureMode currentText
        :param resolution ( type == str ) in format 'width'x'height'
        :return:
        """
        self.set_resolution(resolution)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdditionCameraSettings()
    window.show()
    sys.exit(app.exec())
