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
        self.aamc = ''
        self.ui.exportButton.clicked.connect(self.my_clicked)
        self.ui.horizontalSlider.valueChanged.connect(self.updateLabel)
        self.answer_map = {-1: -1, -6:1, -4:2, -2:3, -5:4, -3:5}
        self.yn_map = {-1: -1, -2:0, -3:1}
        self.questions = [self.ui.likert_1_q, self.ui.likert_2_q, self.ui.likert_3_q, self.ui.likert_4_q,
                               self.ui.likert_5_q, self.ui.likert_6_q, self.ui.likert_7_q, self.ui.likert_8_q,
                               self.ui.likert_9_q, self.ui.likert_10_q, self.ui.likert_11_q, self.ui.likert_12_q,
                               self.ui.likert_13_q ]
        self.questions_txt = [q.text() for q in self.questions]
        self.question_map = dict((txt, i) for i, txt in enumerate(self.questions_txt))
        self.answer_buttons = [self.ui.likert_1_group, self.ui.likert_2_group, self.ui.likert_3_group, self.ui.likert_4_group,
                               self.ui.likert_5_group, self.ui.likert_6_group, self.ui.likert_7_group, self.ui.likert_8_group,
                               self.ui.likert_9_group, self.ui.likert_10_group, self.ui.likert_11_group, self.ui.likert_12_group ,self.ui.likert_13_group ]

    def updateLabel(self, value):
        self.ui.updateLabel.setText(f"{value}%")
    def make_json(self):

        exam = self.ui.comboBox.currentIndex()
        dates, cards, times = self.queryer.get_revs()
        total, unlocked, mature, yng_lrn, new, susp = self.queryer.get_cards()
        hours_dict = self.queryer.get_hour_bkdwn()
        days_doc = [{'date': day, 'cards': card, 'time': time} for day, card, time in
                    zip(dates, cards, times)]
        survey_dict = {}
        for question, answer in zip(self.questions, self.answer_buttons):
            question_str = question.text()
            answer_id = answer.checkedId()
            if question is self.ui.likert_13_q:
                answer_id = self.yn_map[answer_id]
            else:
                answer_id = self.answer_map[answer_id]
            question_id = self.question_map[question_str]
            survey_dict[question_id] = answer_id
        survey_dict[max(self.question_map.values())+1] = self.ui.horizontalSlider.value()
        doc = dict()
        doc['_id'] = self.aamc
        doc['exam'] = exam
        doc['days'] = days_doc
        doc['total_cards'] = total
        doc['unlocked_cards'] = unlocked
        doc['mature_cards'] = mature
        doc['yng_lrn_cards'] = yng_lrn
        doc['new_cards'] = new
        doc['susp_cards'] = susp
        doc['hours'] = hours_dict
        doc['survey'] = survey_dict
        self.doc =  json.dumps(doc, indent=2)

    def aamc_is_valid(self):
        aamc = self.get_aamc()
        # return True
        return aamc.isdigit() and len(aamc) == 8

    def get_aamc(self):
        return self.ui.aamc_entry.text()

    def all_answered(self):
        # return True
        return all([answer.checkedId() != -1 for answer in self.answer_buttons])

    def export(self):
        if self.aamc_is_valid():
            self.aamc = self.get_aamc()
            client = Client()
            self.make_json()
            print(self.doc)
            client.send(self.doc)
            client.send(client.DISCONNECT_MESSAGE)
            self.close()

        else:
            self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().minimum())
            self.ui.aamc_entry.setFocus()

    def my_clicked(self):
        if self.all_answered():
            self.export()
        else:
            self.ui.error_label.setStyleSheet("background-color: red; border: 2px solid black")
            self.ui.error_label.setText("Please answer all of the survey questions.")



