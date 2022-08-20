# This Python file uses the following encoding: utf-8
import sys
import json
from .queryer import Queryer
from .client import Client
from aqt.qt import QApplication, QDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from .gui.forms.anki21.form import Ui_Dialog

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.queryer = Queryer()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.name = ''
        self.nshe = ''
        self.ui.exportButton.clicked.connect(self.my_clicked)
    def make_json(self):
        dates, cards, times = self.queryer.get_revs()
        days_doc = [{'date': day, 'cards': str(card), 'time': str(time)} for day, card, time in
                    zip(dates, cards, times)]

        doc = {}
        doc['_id'] = self.nshe
        doc['name'] = self.name
        doc['days'] = days_doc
        self.json_doc = json.dumps(doc)
    def get_name(self):
        return self.ui.name_entry.text()
    def get_nshe(self):
        return self.ui.nshe_entry.text()
    def set_output(self,data):
        self.ui.output_box.setPlainText(data)
    def my_clicked(self):
        self.name, self.nshe = self.get_name(), self.get_nshe()
        client = Client()
        self.make_json()
        client.send(self.json_doc)
        client.send(client.DISCONNECT_MESSAGE)
        self.close()



