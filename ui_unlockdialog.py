# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unlock.ui'
#
# Created: Sun Mar 20 16:41:58 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(366, 218)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.stackedWidget = QtGui.QStackedWidget(Dialog)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 40, 361, 181))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.unlockButton = QtGui.QPushButton(self.page)
        self.unlockButton.setGeometry(QtCore.QRect(290, 110, 71, 23))
        self.unlockButton.setObjectName("unlockButton")
        self.passwordLineEdit = QtGui.QLineEdit(self.page)
        self.passwordLineEdit.setGeometry(QtCore.QRect(10, 70, 351, 20))
        self.passwordLineEdit.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.unlockTextLabel = QtGui.QLabel(self.page)
        self.unlockTextLabel.setGeometry(QtCore.QRect(10, 40, 351, 20))
        self.unlockTextLabel.setStyleSheet("#unlockTextLabel {\n"
"    font-size: 16px;\n"
"    \n"
"    font-family: \"Segoe UI\";\n"
"}")
        self.unlockTextLabel.setObjectName("unlockTextLabel")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")
        self.listWidget = QtGui.QListWidget(self.page_2)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 191, 121))
        self.listWidget.setObjectName("listWidget")
        self.label = QtGui.QLabel(self.page_2)
        self.label.setGeometry(QtCore.QRect(10, 20, 171, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.page_2)
        self.label_2.setGeometry(QtCore.QRect(210, 40, 141, 20))
        self.label_2.setObjectName("label_2")
        self.browseButton = QtGui.QPushButton(self.page_2)
        self.browseButton.setGeometry(QtCore.QRect(220, 70, 131, 23))
        self.browseButton.setObjectName("browseButton")
        self.listWidgetUnlockButton = QtGui.QPushButton(self.page_2)
        self.listWidgetUnlockButton.setGeometry(QtCore.QRect(260, 130, 91, 23))
        self.listWidgetUnlockButton.setObjectName("listWidgetUnlockButton")
        self.stackedWidget.addWidget(self.page_2)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 371, 51))
        self.frame.setStyleSheet("background-color: rgb(33, 150, 243);")
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(40, 10, 171, 41))
        self.label_3.setStyleSheet("color: white;\n"
"font-size: 30px;\n"
"font: \"Segoe UI\";\n"
"")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 21, 31))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/images/lock.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.unlockButton.setText(QtGui.QApplication.translate("Dialog", "Unlock", None, QtGui.QApplication.UnicodeUTF8))
        self.unlockTextLabel.setText(QtGui.QApplication.translate("Dialog", "Enter password to unlock file:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Select file from current folder", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Or browse exe file to unlock", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("Dialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidgetUnlockButton.setText(QtGui.QApplication.translate("Dialog", "Unlock", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "EXE Locker", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
