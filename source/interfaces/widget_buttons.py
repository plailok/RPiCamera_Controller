# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaces/widget_buttons.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 158)
        Form.setStyleSheet("QFrame{\n"
"                background-color:rgb(179, 170, 200);\n"
"                border-radius: 15px;\n"
"                }\n"
"QPushButton{\n"
"        border-style: outset;\n"
"        border-width: 2px;\n"
"        border-radius: 10px;\n"
"        border-color: beige;\n"
"        background-color: rgb(232, 198, 217);\n"
"        border-radius: 15px;\n"
"        font: 12pt \"Impact\";\n"
"}\n"
"QPushButton:pressed {\n"
"    \n"
"    background-color: rgb(236, 183, 211);\n"
"    border-style: inset;\n"
"}\n"
"\n"
"\n"
"            ")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox.setTitle("")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(-1, 11, -1, 11)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.captureButton = QtWidgets.QPushButton(self.groupBox)
        self.captureButton.setMinimumSize(QtCore.QSize(0, 70))
        self.captureButton.setFlat(False)
        self.captureButton.setObjectName("captureButton")
        self.horizontalLayout.addWidget(self.captureButton)
        self.captureseriesButton = QtWidgets.QPushButton(self.groupBox)
        self.captureseriesButton.setMinimumSize(QtCore.QSize(100, 70))
        self.captureseriesButton.setObjectName("captureseriesButton")
        self.horizontalLayout.addWidget(self.captureseriesButton)
        self.startButton = QtWidgets.QPushButton(self.groupBox)
        self.startButton.setMinimumSize(QtCore.QSize(0, 70))
        self.startButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.indicator = QtWidgets.QLabel(self.groupBox)
        self.indicator.setMaximumSize(QtCore.QSize(40, 40))
        self.indicator.setStyleSheet("QLabel{\n"
"border-radius:20px;\n"
"background-color:white;                                    \n"
"border-color:black;\n"
"}\n"
"                                                ")
        self.indicator.setFrameShape(QtWidgets.QFrame.Box)
        self.indicator.setFrameShadow(QtWidgets.QFrame.Raised)
        self.indicator.setLineWidth(1)
        self.indicator.setMidLineWidth(0)
        self.indicator.setText("")
        self.indicator.setScaledContents(True)
        self.indicator.setAlignment(QtCore.Qt.AlignCenter)
        self.indicator.setWordWrap(True)
        self.indicator.setObjectName("indicator")
        self.horizontalLayout.addWidget(self.indicator)
        self.stopButton = QtWidgets.QPushButton(self.groupBox)
        self.stopButton.setMinimumSize(QtCore.QSize(0, 70))
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.setdefaultButton = QtWidgets.QPushButton(self.groupBox)
        self.setdefaultButton.setMinimumSize(QtCore.QSize(30, 40))
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.setdefaultButton.setFont(font)
        self.setdefaultButton.setStyleSheet("QPushButton{\n"
"font: 11pt \"Impact\";\n"
"}\n"
"")
        self.setdefaultButton.setObjectName("setdefaultButton")
        self.horizontalLayout.addWidget(self.setdefaultButton)
        self.exitButton = QtWidgets.QPushButton(self.groupBox)
        self.exitButton.setMinimumSize(QtCore.QSize(0, 70))
        self.exitButton.setFlat(False)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(3, 2)
        self.horizontalLayout.setStretch(4, 2)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(6, 2)
        self.verticalLayout.addWidget(self.groupBox, 0, QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.captureButton.setText(_translate("Form", "Capture"))
        self.captureseriesButton.setText(_translate("Form", "Capture Series"))
        self.startButton.setText(_translate("Form", "Start Recording"))
        self.stopButton.setText(_translate("Form", "Stop Recording"))
        self.setdefaultButton.setText(_translate("Form", "Set Default"))
        self.exitButton.setText(_translate("Form", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
