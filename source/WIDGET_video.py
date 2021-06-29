import sys

from PyQt5.QtWidgets import QWidget, QApplication

from .interfaces.widget_video import Ui_VideoFrame


class VideoHolder(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_VideoFrame()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoHolder()
    window.show()
    sys.exit(app.exec())
