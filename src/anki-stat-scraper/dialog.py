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
import re


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.queryer = Queryer()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.name = ''
        self.nshe = ''
        self.ui.exportButton.clicked.connect(self.my_clicked)
        self.answer_map = {-1: -1, -6:1, -4:2, -2:3, -5:4, -3:5}
        self.questions = [self.ui.likert_1_q, self.ui.likert_2_q, self.ui.likert_3_q, self.ui.likert_4_q,
                               self.ui.likert_5_q, self.ui.likert_6_q, self.ui.likert_7_q, self.ui.likert_8_q,
                               self.ui.likert_9_q, self.ui.likert_10_q, self.ui.likert_11_q, self.ui.likert_12_q ]
        self.questions_txt = [q.text() for q in self.questions]
        self.question_map = dict((txt, i) for i, txt in enumerate(self.questions_txt))
        self.answer_buttons = [self.ui.likert_1_group, self.ui.likert_2_group, self.ui.likert_3_group, self.ui.likert_4_group,
                               self.ui.likert_5_group, self.ui.likert_6_group, self.ui.likert_7_group, self.ui.likert_8_group,
                               self.ui.likert_9_group, self.ui.likert_10_group, self.ui.likert_11_group, self.ui.likert_12_group ]
    def make_json(self):

        dates, cards, times = self.queryer.get_revs()
        total, unlocked = self.queryer.get_cards()
        hours_dict = self.queryer.get_hour_bkdwn()
        days_doc = [{'date': day, 'cards': card, 'time': time} for day, card, time in
                    zip(dates, cards, times)]
        survey_dict = {}
        for question, answer in zip(self.questions, self.answer_buttons):
            question_str = question.text()
            answer_id = answer.checkedId()
            answer_id = self.answer_map[answer_id]
            question_id = self.question_map[question_str]
            survey_dict[question_id] = answer_id
        survey_dict[max(self.question_map.values())+1] = self.ui.horizontalSlider.value()
        doc = dict()
        doc['_id'] = self.nshe
        doc['name'] = self.name
        doc['days'] = days_doc
        doc['total_cards'] = total
        doc['unlocked_cards'] = unlocked
        doc['hours'] = hours_dict
        doc['survey'] = survey_dict
        return json.dumps(doc, indent=2)


    def name_is_valid(self):
        name = self.get_name()
        return name.isalpha()
    def nshe_is_valid(self):
        nshe = self.get_nshe()
        return nshe.isdigit()
    def get_name(self):
        return self.ui.name_entry.text()
    def get_nshe(self):
        return self.ui.nshe_entry.text()
    def my_clicked(self):
        self.name, self.nshe = self.get_name(), self.get_nshe()
        if self.name_is_valid() and self.nshe_is_valid():

            client = Client()
            doc = self.make_json()
            print(doc)
            client.send(doc)
            client.send(client.DISCONNECT_MESSAGE)
            self.close()

        elif not self.name_is_valid():
            self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().minimum())
            self.ui.name_entry.setFocus()
        else:
            self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().minimum())
            self.ui.nshe_entry.setFocus()


