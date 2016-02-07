import sys
from PySide import QtCore

from PySide.QtGui import QDialog, QApplication

import ui_maindialog

class LockerDialog(QDialog, ui_maindialog.Ui_MainDialog):
    def __init__(self, parent=None):
        super(LockerDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint )
        self.setFixedSize(self.width(), self.height())
        self.lockButton.setEnabled(False) # lock the exe button still password is set


app = QApplication(sys.argv)
locker = LockerDialog()
locker.show()
app.exec_()


