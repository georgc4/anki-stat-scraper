# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(800, 600)
        self.exportButton = QPushButton(Dialog)
        self.exportButton.setObjectName(u"exportButton")
        self.exportButton.setGeometry(QRect(350, 390, 80, 25))
        self.name_container = QWidget(Dialog)
        self.name_container.setObjectName(u"name_container")
        self.name_container.setGeometry(QRect(60, 100, 120, 80))
        self.name_label = QLabel(self.name_container)
        self.name_label.setObjectName(u"name_label")
        self.name_label.setGeometry(QRect(0, 10, 51, 17))
        self.name_entry = QLineEdit(self.name_container)
        self.name_entry.setObjectName(u"name_entry")
        self.name_entry.setGeometry(QRect(0, 30, 113, 25))
        self.nshe_container = QWidget(Dialog)
        self.nshe_container.setObjectName(u"nshe_container")
        self.nshe_container.setGeometry(QRect(210, 100, 120, 80))
        self.nshe_label = QLabel(self.nshe_container)
        self.nshe_label.setObjectName(u"nshe_label")
        self.nshe_label.setGeometry(QRect(0, 10, 51, 17))
        self.nshe_entry = QLineEdit(self.nshe_container)
        self.nshe_entry.setObjectName(u"nshe_entry")
        self.nshe_entry.setGeometry(QRect(0, 30, 113, 25))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.exportButton.setText(QCoreApplication.translate("Dialog", u"Export", None))
        self.name_label.setText(QCoreApplication.translate("Dialog", u"Name:*", None))
        self.nshe_label.setText(QCoreApplication.translate("Dialog", u"NSHE:*", None))
    # retranslateUi

