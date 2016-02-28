import sys

import time
from PySide import QtCore, QtGui
from PySide.QtCore import QThread, SIGNAL, Qt, Signal, QObject

from PySide.QtGui import QDialog, QApplication, QMessageBox, QFileDialog

import ui_maindialog
from EXELockerFile.Encryptor import EncryptedFile
import admin

__appname__ = "EXE Locker"

class LockerDialog(QDialog, ui_maindialog.Ui_MainDialog):
    signal = Signal(str)

    def __init__(self, parent=None):
        super(LockerDialog, self).__init__(parent)
        if not admin.isUserAdmin():
            admin.runAsAdmin()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setFixedSize(self.width(), self.height())
        self.lockButton.setEnabled(False)  # lock the exe button still password is set
        self.pickFileButton.clicked.connect(self.showFileDialog)
        self.passwordLineEdit.textChanged.connect(self.checkPasswordMatch)
        self.passwordAgainLineEdit.textChanged.connect(self.checkPasswordMatch)
        self.lockButton.clicked.connect(self._lockFile)
        # Connect to threadDone event
        self.signal.connect(self.fileLockedEvent)



    def fileLockedEvent(self, fileName):
        msgSuccess = "{0} locked successfully.".format(fileName)
        QMessageBox.information(self, __appname__, msgSuccess)
        self.lockButton.setText("Lock EXE")
        self.lockButton.setEnabled(True)
        self.groupBox.setEnabled(True)
        self.step1GroupBox.setEnabled(True)


    def showFileDialog(self):
        dir = "."
        fileObj = QFileDialog.getOpenFileName(self, "Select Executable to lock", dir="", filter="EXE file (*.exe)")
        if len(fileObj) > 0:
            self.locationLineEdit.setText(fileObj[0])
        else:
            return None


    def checkPasswordMatch(self):
        if self._passwordNotEmpty() and self._passwordEquals():
            self.lockButton.setEnabled(True)
            self.label_4.setVisible(False)
        else:
            self.lockButton.setEnabled(False)
            self.label_4.setVisible(True)


    def _passwordNotEmpty(self):
        if len(self.passwordLineEdit.text()) == 0 or len(self.passwordAgainLineEdit.text()) == 0:
            return False
        else:
            return True


    def _passwordEquals(self):
        if self.passwordLineEdit.text() == self.passwordAgainLineEdit.text():
            return True
        else:
            return False


    def _lockFile(self):
        fileName = self.locationLineEdit.text()
        if len(self.locationLineEdit.text()) == 0 or self.locationLineEdit.text() == None:
            QMessageBox.information(self, __appname__, "Pick an exe file first to lock.")
            self.showFileDialog()
        else:
            password = self.passwordLineEdit.text()
            makeBackup = self.checkBox.isChecked()
            self.workerThread = WorkerThread(fileName, password, self.signal, makeBackup)
            self.lockButton.setText("Working")
            self.lockButton.setEnabled(False)
            self.groupBox.setEnabled(False)
            self.step1GroupBox.setEnabled(False)
            self.workerThread.start()


class WorkerThread(QThread):
    def __init__(self, fileName, password, signal, makeBackup = False, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.fileName = fileName
        self.signal = signal
        self.password = password
        self.makeBackup = makeBackup
    def run(self):
        file = EncryptedFile.createEncryptedFile(self.fileName, self.password, makeBackup=self.makeBackup)
        self.signal.emit(self.fileName)


app = QApplication(sys.argv)
locker = LockerDialog()
locker.show()
app.exec_()
