import os
import sys

from PySide.QtCore import QThread, QObject

from EXELockerFile.EncryptionHelper import EncryptionHelper
from ui_unlockdialog import Ui_Dialog
from PySide import QtCore, QtGui
from PySide.QtGui import QDialog, QApplication, QMessageBox, QFileDialog
import admin
from EXELockerFile.Encryptor import EncryptedFile

__appname__ = "EXE Locker"


class UnlockDialog(QDialog, Ui_Dialog):
    signal = QtCore.Signal(str, str)

    def __init__(self, fileName=None, parent=None):
        super(UnlockDialog, self).__init__(parent)
        if not admin.isUserAdmin():
            admin.runAsAdmin()
            # end the current instance of the program because it isn't uac. Results in two app windows otherwise.
            sys.exit(0)
        self.setupUi(self)
        fileArgPos = self._getRelevantCmdArgument(sys.argv)
        if fileArgPos != None:
            self.fileName = sys.argv[fileArgPos]
            self.stackedWidget.setCurrentIndex(0)
            self.setUnlockTextLabel(self.fileName)
            self.sameLocation = False
        elif self._checkScriptNameInFolder():
            scriptName = os.path.basename(__file__)
            # get the script name without file extension
            scriptName = os.path.splitext(scriptName)[0] + ".exelocker"
            self.fileName = os.path.basename(scriptName)
            self.sameLocation = True
            self.setUnlockTextLabel(self.fileName)
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.fileName = None
            self.sameLocation = True
            self.stackedWidget.setCurrentIndex(1)
            self.fillListWidget()

        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setFixedSize(self.width(), self.height())

        # connect the unlock button
        self.unlockButton.clicked.connect(self.unlockFile)
        self.passwordLineEdit.returnPressed.connect(self.unlockFile)
        self.browseButton.clicked.connect(self.browseFiles)
        self.listWidgetUnlockButton.clicked.connect(self.listWidgetSelectedEvent)


        # connect with the thread
        self.signal.connect(self.fileUnlockedEvent)

    def _checkScriptNameInFolder(self):
        scriptName = os.path.basename(__file__)
        # get script name without extension
        scriptName = os.path.splitext(scriptName)[0]
        # change extension of script name to lock to .exelocker
        scriptName = scriptName + ".exelocker"
        fileList = self._getRelevantFilesInFolder()
        try:
            index = fileList.index(scriptName)
        except ValueError:
            index = None
        if index != None:
            return True
        else:
            return False

    def listWidgetSelectedEvent(self):
        self.fileName = self.listWidget.currentItem().text()
        self.setUnlockTextLabel(self.fileName)
        self.stackedWidget.setCurrentIndex(0)
        self.setUnlockTextLabel(self.fileName)

    def setUnlockTextLabel(self, fileName):
        if fileName and len(fileName):
            fileName = os.path.basename(fileName)
            string = u"Enter password for " + fileName + ":"
            self.unlockTextLabel.setText(string)

    def fillListWidget(self):
        filteredList = self._getRelevantFilesInFolder()
        self.listWidget.addItems(filteredList)

    def _getRelevantFilesInFolder(self):
        files = os.listdir('.')
        filteredList = []
        for f in files:
            if os.path.isfile(f):
                extension = os.path.splitext(f)[1]
                if extension == ".exelocker":
                    filteredList.append(f)
        return filteredList

    def browseFiles(self):
        dir = "."
        file = QFileDialog.getOpenFileName(self, "Select .exelocker file", dir, "EXE Locker file (*.exelocker)")
        if len(file[0]):
            self.fileName = file[0]
            self.stackedWidget.setCurrentIndex(0)
            self.setUnlockTextLabel(self.fileName)

    def fileUnlockedEvent(self, success, decryptedFileName):
        if success == 'True':
            QMessageBox.information(self, __appname__, "File Unlocked Successfully.")
        else:
            os.remove(decryptedFileName)
            QMessageBox.information(self, __appname__, "Wrong password. Couldn't unlock file.")

    def unlockFile(self):
        if EncryptedFile.isValidFile(self.fileName):
            eFile = EncryptedFile(self.fileName)
            unhashedPassword = self.passwordLineEdit.text()
            password = EncryptionHelper.generateKeyHash(unhashedPassword)
            self.thread = QThread()
            self.worker = Worker(eFile, password, self.signal, self.sameLocation)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.signal.connect(self.thread.quit)
            self.worker.signal.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
        else:
            QMessageBox.information(self, __appname__, "Invalid .exelocker file.")
        self.passwordLineEdit.setText("")



    def _getRelevantCmdArgument(self, args):
        for arg in args:
            if EncryptedFile.isValidFile(arg):
                return args.index(arg)

        return None

class Worker(QObject):
    def __init__(self, unencryptedFile, password, signal, sameLocation = False, parent=None):
        super(Worker, self).__init__(parent)
        self.decryptedFileName = unencryptedFile.getOriginalFileName()
        self.unencryptedFile = unencryptedFile
        self.signal = signal
        self.password = password
        self.sameLocation = sameLocation

    def run(self):
        self.unencryptedFile.decryptFile(self.password, self.sameLocation)
        checksum = EncryptionHelper.generateFileChecksum(self.decryptedFileName)
        if checksum == self.unencryptedFile.getChecksum():
            self.signal.emit('True', self.decryptedFileName)
        else:
            self.signal.emit('False', self.decryptedFileName)

app = QApplication(sys.argv)
unlocker = UnlockDialog()
unlocker.show()
app.exec_()
