# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'languagestFRzNm.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_LanguageDlg(object):
    def setupUi(self, LanguageDlg):
        if not LanguageDlg.objectName():
            LanguageDlg.setObjectName(u"LanguageDlg")
        LanguageDlg.resize(333, 278)
        self.vboxLayout = QVBoxLayout(LanguageDlg)
        self.vboxLayout.setSpacing(6)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.vboxLayout.setContentsMargins(9, 9, 9, 9)
        self.frame = QFrame(LanguageDlg)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.en_rbt = QRadioButton(self.frame)
        self.en_rbt.setObjectName(u"en_rbt")

        self.verticalLayout.addWidget(self.en_rbt)

        self.pt_BR_rbt = QRadioButton(self.frame)
        self.pt_BR_rbt.setObjectName(u"pt_BR_rbt")

        self.verticalLayout.addWidget(self.pt_BR_rbt)

        self.spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.spacerItem)


        self.vboxLayout.addWidget(self.frame)

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setSpacing(6)
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.hboxLayout.setContentsMargins(0, 0, 0, 0)
        self.spacerItem1 = QSpacerItem(131, 31, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hboxLayout.addItem(self.spacerItem1)

        self.okButton = QPushButton(LanguageDlg)
        self.okButton.setObjectName(u"okButton")

        self.hboxLayout.addWidget(self.okButton)

        self.cancelButton = QPushButton(LanguageDlg)
        self.cancelButton.setObjectName(u"cancelButton")

        self.hboxLayout.addWidget(self.cancelButton)


        self.vboxLayout.addLayout(self.hboxLayout)


        self.retranslateUi(LanguageDlg)
        self.okButton.clicked.connect(LanguageDlg.accept)
        self.cancelButton.clicked.connect(LanguageDlg.reject)

        QMetaObject.connectSlotsByName(LanguageDlg)
    # setupUi

    def retranslateUi(self, LanguageDlg):
        LanguageDlg.setWindowTitle(QCoreApplication.translate("LanguageDlg", u"Dialog", None))
        self.en_rbt.setText(QCoreApplication.translate("LanguageDlg", u"English", None))
        self.pt_BR_rbt.setText(QCoreApplication.translate("LanguageDlg", u"Portuguese (BR)", None))
        self.okButton.setText(QCoreApplication.translate("LanguageDlg", u"OK", None))
        self.cancelButton.setText(QCoreApplication.translate("LanguageDlg", u"Cancel", None))
    # retranslateUi

