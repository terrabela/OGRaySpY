# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ograyspy_mainXqoXiI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_Open_a_spectrum = QAction(MainWindow)
        self.action_Open_a_spectrum.setObjectName(u"action_Open_a_spectrum")
        self.actionGenerate_report = QAction(MainWindow)
        self.actionGenerate_report.setObjectName(u"actionGenerate_report")
        self.actionP_lots = QAction(MainWindow)
        self.actionP_lots.setObjectName(u"actionP_lots")
        self.actionPandas_dataframe = QAction(MainWindow)
        self.actionPandas_dataframe.setObjectName(u"actionPandas_dataframe")
        self.actionE_xit = QAction(MainWindow)
        self.actionE_xit.setObjectName(u"actionE_xit")
        self.actionLanguages = QAction(MainWindow)
        self.actionLanguages.setObjectName(u"actionLanguages")
        self.actionChoose_a_spectrum = QAction(MainWindow)
        self.actionChoose_a_spectrum.setObjectName(u"actionChoose_a_spectrum")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menu_Settings = QMenu(self.menubar)
        self.menu_Settings.setObjectName(u"menu_Settings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Settings.menuAction())
        self.menuFile.addAction(self.action_Open_a_spectrum)
        self.menuFile.addAction(self.actionChoose_a_spectrum)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionGenerate_report)
        self.menuFile.addAction(self.actionP_lots)
        self.menuFile.addAction(self.actionPandas_dataframe)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionE_xit)
        self.menu_Settings.addAction(self.actionLanguages)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OGRaySpY", None))
        self.action_Open_a_spectrum.setText(QCoreApplication.translate("MainWindow", u"&Open a spectrum", None))
        self.actionGenerate_report.setText(QCoreApplication.translate("MainWindow", u"Generate &report", None))
        self.actionP_lots.setText(QCoreApplication.translate("MainWindow", u"P&lots", None))
        self.actionPandas_dataframe.setText(QCoreApplication.translate("MainWindow", u"Pandas &dataframe", None))
        self.actionE_xit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
        self.actionLanguages.setText(QCoreApplication.translate("MainWindow", u"Languages", None))
        self.actionChoose_a_spectrum.setText(QCoreApplication.translate("MainWindow", u"Choose a spectrum", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_Settings.setTitle(QCoreApplication.translate("MainWindow", u"&Settings", None))
    # retranslateUi

