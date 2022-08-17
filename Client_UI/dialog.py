# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from .ui_form import Ui_Dialog

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.name = ''
        self.nshe = ''
        self.ui.exportButton.clicked.connect(self.my_clicked)
    def get_name(self):
        return self.ui.name_entry.text()
    def get_nshe(self):
        return self.ui.nshe_entry.text()
    def my_clicked(self):
        self.name, self.nshe = self.get_name(), self.get_nshe()
        self.close()



def main():
    app = QApplication.instance()
    widget = Dialog()
    widget.exec_()
    return widget.name, widget.nshe