import sys
from PySide import QtCore

from PySide.QtGui import QDialog, QApplication

import ui_maindialog

class LockerDialog(QDialog, ui_maindialog.Ui_MainDialog):
    def __init__(self, parent=None):
        super(LockerDialog, self).__init__(parent)
        self.setupUi(self)



app = QApplication(sys.argv)
locker = LockerDialog()
locker.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint )
locker.show()
locker.setFixedSize(locker.width(), locker.height())
app.exec_()
