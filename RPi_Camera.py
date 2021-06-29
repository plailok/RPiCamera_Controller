import sys

from PyQt5.QtWidgets import QApplication

from source.MAIN_WINDOW import MyWindow


class ApplicationMainWindow(MyWindow):
    """
    Created by Oleksandr M.
    Created for:
        ICS => (Institute of Complex System)
            LOSIP => (Laboratory of Signals and Image Processing)
    
    This is MainWindow loader.
        To run it use python3 RPi_Camera.py in console
        28.06.2021 => No argparser avaliable
    
    Every Exeprion automaticly added to Rpi_Camera_log.log
        if any occure you can send .log file or sreenshoot to frozon201@gmail.com
        
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ApplicationMainWindow()
    window.show()
    sys.exit(app.exec())
