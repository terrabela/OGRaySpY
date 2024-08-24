# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spectrumform_with_ok_canceldHGjXC.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(938, 590)
        self.verticalLayout_7 = QVBoxLayout(Dialog)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.verticalLayout_9 = QVBoxLayout(self.tab_9)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.rawDataTed = QTextEdit(self.tab_9)
        self.rawDataTed.setObjectName(u"rawDataTed")

        self.verticalLayout_9.addWidget(self.rawDataTed)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)

        self.pbtRoot = QPushButton(self.tab_9)
        self.pbtRoot.setObjectName(u"pbtRoot")

        self.horizontalLayout_9.addWidget(self.pbtRoot)


        self.verticalLayout_9.addLayout(self.horizontalLayout_9)

        self.tabWidget.addTab(self.tab_9, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_2 = QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabulatedDataTbv = QTableView(self.tab)
        self.tabulatedDataTbv.setObjectName(u"tabulatedDataTbv")

        self.horizontalLayout_2.addWidget(self.tabulatedDataTbv)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout = QHBoxLayout(self.tab_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout = QGridLayout(self.tab_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_6 = QGroupBox(self.tab_3)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.sampDescrTed = QTextEdit(self.groupBox_6)
        self.sampDescrTed.setObjectName(u"sampDescrTed")

        self.verticalLayout_5.addWidget(self.sampDescrTed)


        self.gridLayout.addWidget(self.groupBox_6, 0, 0, 1, 1)

        self.groupBox_7 = QGroupBox(self.tab_3)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.formLayout_4 = QFormLayout(self.groupBox_7)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.label_15 = QLabel(self.groupBox_7)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_15)

        self.startDte = QDateTimeEdit(self.groupBox_7)
        self.startDte.setObjectName(u"startDte")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.startDte)

        self.label_23 = QLabel(self.groupBox_7)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_23)

        self.label_13 = QLabel(self.groupBox_7)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_13)

        self.leLT_2 = QLineEdit(self.groupBox_7)
        self.leLT_2.setObjectName(u"leLT_2")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.leLT_2)

        self.label_12 = QLabel(self.groupBox_7)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_12)

        self.leRT_2 = QLineEdit(self.groupBox_7)
        self.leRT_2.setObjectName(u"leRT_2")

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.leRT_2)

        self.label_17 = QLabel(self.groupBox_7)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.label_17)

        self.leDelayInDays = QLineEdit(self.groupBox_7)
        self.leDelayInDays.setObjectName(u"leDelayInDays")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.leDelayInDays)

        self.leNoCh_2 = QLineEdit(self.groupBox_7)
        self.leNoCh_2.setObjectName(u"leNoCh_2")
        self.leNoCh_2.setReadOnly(True)

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.leNoCh_2)


        self.gridLayout.addWidget(self.groupBox_7, 0, 1, 1, 1)

        self.groupBox_8 = QGroupBox(self.tab_3)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self._4 = QGridLayout(self.groupBox_8)
        self._4.setSpacing(6)
        self._4.setObjectName(u"_4")
        self._4.setContentsMargins(8, 8, 8, 8)
        self.label_18 = QLabel(self.groupBox_8)
        self.label_18.setObjectName(u"label_18")

        self._4.addWidget(self.label_18, 1, 3, 1, 1)

        self.leUncertainty_2 = QLineEdit(self.groupBox_8)
        self.leUncertainty_2.setObjectName(u"leUncertainty_2")

        self._4.addWidget(self.leUncertainty_2, 1, 2, 1, 1)

        self.label_19 = QLabel(self.groupBox_8)
        self.label_19.setObjectName(u"label_19")

        self._4.addWidget(self.label_19, 1, 0, 1, 2)

        self.cbUnit_2 = QComboBox(self.groupBox_8)
        self.cbUnit_2.addItem("")
        self.cbUnit_2.addItem("")
        self.cbUnit_2.addItem("")
        self.cbUnit_2.addItem("")
        self.cbUnit_2.addItem("")
        self.cbUnit_2.setObjectName(u"cbUnit_2")

        self._4.addWidget(self.cbUnit_2, 0, 4, 1, 1)

        self.leValue_2 = QLineEdit(self.groupBox_8)
        self.leValue_2.setObjectName(u"leValue_2")

        self._4.addWidget(self.leValue_2, 0, 1, 1, 3)

        self.label_20 = QLabel(self.groupBox_8)
        self.label_20.setObjectName(u"label_20")

        self._4.addWidget(self.label_20, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_8, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_3 = QGridLayout(self.tab_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox_5 = QGroupBox(self.tab_4)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.formLayout_3 = QFormLayout(self.groupBox_5)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.label_22 = QLabel(self.groupBox_5)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_22)

        self.cbxSelectedAnalysisLib = QComboBox(self.groupBox_5)
        self.cbxSelectedAnalysisLib.setObjectName(u"cbxSelectedAnalysisLib")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.cbxSelectedAnalysisLib)

        self.label_21 = QLabel(self.groupBox_5)
        self.label_21.setObjectName(u"label_21")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_21)

        self.cbxSelectedCalibLib = QComboBox(self.groupBox_5)
        self.cbxSelectedCalibLib.setObjectName(u"cbxSelectedCalibLib")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.cbxSelectedCalibLib)


        self.gridLayout_3.addWidget(self.groupBox_5, 0, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.tab_4)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.formLayout_2 = QFormLayout(self.groupBox_4)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.leNoFwhmOfPeak = QLineEdit(self.groupBox_4)
        self.leNoFwhmOfPeak.setObjectName(u"leNoFwhmOfPeak")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.leNoFwhmOfPeak)

        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.leNoFwhmOfSideBaseline = QLineEdit(self.groupBox_4)
        self.leNoFwhmOfSideBaseline.setObjectName(u"leNoFwhmOfSideBaseline")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.leNoFwhmOfSideBaseline)

        self.label = QLabel(self.groupBox_4)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label)

        self.cbxTypeBaseline = QComboBox(self.groupBox_4)
        self.cbxTypeBaseline.addItem("")
        self.cbxTypeBaseline.addItem("")
        self.cbxTypeBaseline.addItem("")
        self.cbxTypeBaseline.setObjectName(u"cbxTypeBaseline")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.cbxTypeBaseline)

        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_9)

        self.leBaselinePolyGrade = QLineEdit(self.groupBox_4)
        self.leBaselinePolyGrade.setObjectName(u"leBaselinePolyGrade")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.leBaselinePolyGrade)

        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.cbxInterpolationMethod = QComboBox(self.groupBox_4)
        self.cbxInterpolationMethod.addItem("")
        self.cbxInterpolationMethod.addItem("")
        self.cbxInterpolationMethod.setObjectName(u"cbxInterpolationMethod")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.cbxInterpolationMethod)

        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_14)

        self.cbxFitStrategy = QComboBox(self.groupBox_4)
        self.cbxFitStrategy.addItem("")
        self.cbxFitStrategy.addItem("")
        self.cbxFitStrategy.setObjectName(u"cbxFitStrategy")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.cbxFitStrategy)


        self.gridLayout_3.addWidget(self.groupBox_4, 1, 0, 1, 1)

        self.groupBox = QGroupBox(self.tab_4)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout_5 = QFormLayout(self.groupBox)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_11)

        self.leToler = QLineEdit(self.groupBox)
        self.leToler.setObjectName(u"leToler")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.leToler)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.label_16)


        self.gridLayout_3.addWidget(self.groupBox, 1, 1, 1, 1)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.tab_5)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.cbxEnChFitType = QComboBox(self.tab_5)
        self.cbxEnChFitType.addItem("")
        self.cbxEnChFitType.addItem("")
        self.cbxEnChFitType.setObjectName(u"cbxEnChFitType")

        self.verticalLayout_3.addWidget(self.cbxEnChFitType)

        self.enxchanTbv = QTableView(self.tab_5)
        self.enxchanTbv.setObjectName(u"enxchanTbv")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enxchanTbv.sizePolicy().hasHeightForWidth())
        self.enxchanTbv.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.enxchanTbv)

        self.doEnChFitPbt = QPushButton(self.tab_5)
        self.doEnChFitPbt.setObjectName(u"doEnChFitPbt")

        self.verticalLayout_3.addWidget(self.doEnChFitPbt)

        self.pbtClearEnergyCalibration = QPushButton(self.tab_5)
        self.pbtClearEnergyCalibration.setObjectName(u"pbtClearEnergyCalibration")

        self.verticalLayout_3.addWidget(self.pbtClearEnergyCalibration)

        self.pbtAcceptNewEnergies = QPushButton(self.tab_5)
        self.pbtAcceptNewEnergies.setObjectName(u"pbtAcceptNewEnergies")

        self.verticalLayout_3.addWidget(self.pbtAcceptNewEnergies)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_3 = QLabel(self.tab_5)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_4.addWidget(self.label_3)

        self.cbxFwhmChFitType = QComboBox(self.tab_5)
        self.cbxFwhmChFitType.addItem("")
        self.cbxFwhmChFitType.addItem("")
        self.cbxFwhmChFitType.setObjectName(u"cbxFwhmChFitType")

        self.verticalLayout_4.addWidget(self.cbxFwhmChFitType)

        self.fwhmxenTbv = QTableView(self.tab_5)
        self.fwhmxenTbv.setObjectName(u"fwhmxenTbv")

        self.verticalLayout_4.addWidget(self.fwhmxenTbv)

        self.doFwhmChFitPbt = QPushButton(self.tab_5)
        self.doFwhmChFitPbt.setObjectName(u"doFwhmChFitPbt")

        self.verticalLayout_4.addWidget(self.doFwhmChFitPbt)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.groupBox_3 = QGroupBox(self.tab_5)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.tlBinFiltGr = QLabel(self.groupBox_3)
        self.tlBinFiltGr.setObjectName(u"tlBinFiltGr")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.tlBinFiltGr)

        self.leBinFiltGr = QLineEdit(self.groupBox_3)
        self.leBinFiltGr.setObjectName(u"leBinFiltGr")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leBinFiltGr)

        self.tlPkcut = QLabel(self.groupBox_3)
        self.tlPkcut.setObjectName(u"tlPkcut")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.tlPkcut)

        self.lePkcut = QLineEdit(self.groupBox_3)
        self.lePkcut.setObjectName(u"lePkcut")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lePkcut)

        self.tlSideChannelsSearch = QLabel(self.groupBox_3)
        self.tlSideChannelsSearch.setObjectName(u"tlSideChannelsSearch")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.tlSideChannelsSearch)

        self.leSideChannelsSearch = QLineEdit(self.groupBox_3)
        self.leSideChannelsSearch.setObjectName(u"leSideChannelsSearch")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.leSideChannelsSearch)


        self.verticalLayout_8.addLayout(self.formLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_2.addWidget(self.label_10)

        self.energypointsTbv = QTableView(self.groupBox_3)
        self.energypointsTbv.setObjectName(u"energypointsTbv")
        sizePolicy.setHeightForWidth(self.energypointsTbv.sizePolicy().hasHeightForWidth())
        self.energypointsTbv.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.energypointsTbv)

        self.pbtNewSearch = QPushButton(self.groupBox_3)
        self.pbtNewSearch.setObjectName(u"pbtNewSearch")

        self.verticalLayout_2.addWidget(self.pbtNewSearch)


        self.verticalLayout_8.addLayout(self.verticalLayout_2)


        self.horizontalLayout_4.addWidget(self.groupBox_3)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.tab_6.setEnabled(True)
        self.horizontalLayout_5 = QHBoxLayout(self.tab_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.tab_6)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.neffptsLne = QLineEdit(self.tab_6)
        self.neffptsLne.setObjectName(u"neffptsLne")

        self.horizontalLayout_3.addWidget(self.neffptsLne)

        self.doefficfitPbt = QPushButton(self.tab_6)
        self.doefficfitPbt.setObjectName(u"doefficfitPbt")

        self.horizontalLayout_3.addWidget(self.doefficfitPbt)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.efficPtsTbv = QTableView(self.tab_6)
        self.efficPtsTbv.setObjectName(u"efficPtsTbv")

        self.verticalLayout_6.addWidget(self.efficPtsTbv)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_4 = QLabel(self.tab_6)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_8.addWidget(self.label_4)

        self.polygradeLne = QLineEdit(self.tab_6)
        self.polygradeLne.setObjectName(u"polygradeLne")

        self.horizontalLayout_8.addWidget(self.polygradeLne)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.effxenTbv = QTableView(self.tab_6)
        self.effxenTbv.setObjectName(u"effxenTbv")

        self.verticalLayout_6.addWidget(self.effxenTbv)


        self.horizontalLayout_5.addLayout(self.verticalLayout_6)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.verticalLayout_10 = QVBoxLayout(self.tab_10)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.gammasPerNuclideTbv = QTableView(self.tab_10)
        self.gammasPerNuclideTbv.setObjectName(u"gammasPerNuclideTbv")

        self.verticalLayout_10.addWidget(self.gammasPerNuclideTbv)

        self.tabWidget.addTab(self.tab_10, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.horizontalLayout_7 = QHBoxLayout(self.tab_7)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.fittedPeaksTbv = QTableView(self.tab_7)
        self.fittedPeaksTbv.setObjectName(u"fittedPeaksTbv")

        self.horizontalLayout_7.addWidget(self.fittedPeaksTbv)

        self.tabWidget.addTab(self.tab_7, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.verticalLayout = QVBoxLayout(self.tab_11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.activitiesTbv = QTableView(self.tab_11)
        self.activitiesTbv.setObjectName(u"activitiesTbv")

        self.verticalLayout.addWidget(self.activitiesTbv)

        self.partialActivitiesTbv = QTableView(self.tab_11)
        self.partialActivitiesTbv.setObjectName(u"partialActivitiesTbv")

        self.verticalLayout.addWidget(self.partialActivitiesTbv)

        self.tabWidget.addTab(self.tab_11, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.horizontalLayout_6 = QHBoxLayout(self.tab_8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pteWidthFitLog = QPlainTextEdit(self.tab_8)
        self.pteWidthFitLog.setObjectName(u"pteWidthFitLog")

        self.horizontalLayout_6.addWidget(self.pteWidthFitLog)

        self.pteBaseLinesFitLog = QPlainTextEdit(self.tab_8)
        self.pteBaseLinesFitLog.setObjectName(u"pteBaseLinesFitLog")

        self.horizontalLayout_6.addWidget(self.pteBaseLinesFitLog)

        self.tabWidget.addTab(self.tab_8, "")
        self.splitter.addWidget(self.tabWidget)
        self.buttonBox = QDialogButtonBox(self.splitter)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.splitter.addWidget(self.buttonBox)

        self.verticalLayout_7.addWidget(self.splitter)

#if QT_CONFIG(shortcut)
        self.label_15.setBuddy(self.startDte)
        self.label_13.setBuddy(self.leLT_2)
        self.label_12.setBuddy(self.leRT_2)
        self.label_17.setBuddy(self.leNoCh_2)
        self.label_22.setBuddy(self.leNoFwhmOfPeak)
        self.label_21.setBuddy(self.leNoFwhmOfSideBaseline)
        self.label_8.setBuddy(self.leNoFwhmOfPeak)
        self.label_7.setBuddy(self.leNoFwhmOfSideBaseline)
        self.label.setBuddy(self.cbxTypeBaseline)
        self.label_9.setBuddy(self.leBaselinePolyGrade)
        self.label_5.setBuddy(self.cbxTypeBaseline)
        self.label_14.setBuddy(self.cbxTypeBaseline)
        self.tlSideChannelsSearch.setBuddy(self.leSideChannelsSearch)
        self.label_6.setBuddy(self.neffptsLne)
        self.label_4.setBuddy(self.polygradeLne)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pbtRoot.setText(QCoreApplication.translate("Dialog", u"Call ROOT", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), QCoreApplication.translate("Dialog", u"Raw data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Tabulated data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Spectrum Plot", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Dialog", u"Sample description", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Dialog", u"Acquisition", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Start of acquisition", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Delay in days", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Live time:", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Real time:", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Number of channels:", None))
        self.leDelayInDays.setText(QCoreApplication.translate("Dialog", u"13", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Dialog", u"Quantity", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"%", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Uncertainty:", None))
        self.cbUnit_2.setItemText(0, QCoreApplication.translate("Dialog", u"L", None))
        self.cbUnit_2.setItemText(1, QCoreApplication.translate("Dialog", u"mL", None))
        self.cbUnit_2.setItemText(2, QCoreApplication.translate("Dialog", u"g", None))
        self.cbUnit_2.setItemText(3, QCoreApplication.translate("Dialog", u"kg", None))
        self.cbUnit_2.setItemText(4, QCoreApplication.translate("Dialog", u"sample", None))

        self.label_20.setText(QCoreApplication.translate("Dialog", u"Value:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Sample", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"Nuclide libraries", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Analysis library:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Calibration library:", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Peak Fit", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"# Fwhms for each peak:", None))
        self.leNoFwhmOfPeak.setInputMask("")
        self.leNoFwhmOfPeak.setText(QCoreApplication.translate("Dialog", u"4,0", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"# Fwhms for each side baseline", None))
        self.leNoFwhmOfSideBaseline.setText(QCoreApplication.translate("Dialog", u"5,0", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Function type of baselines:", None))
        self.cbxTypeBaseline.setItemText(0, QCoreApplication.translate("Dialog", u"Exponential", None))
        self.cbxTypeBaseline.setItemText(1, QCoreApplication.translate("Dialog", u"Polynomial", None))
        self.cbxTypeBaseline.setItemText(2, QCoreApplication.translate("Dialog", u"Exponential + constant", None))

        self.label_9.setText(QCoreApplication.translate("Dialog", u"Grade of polynomial for side baselines:", None))
        self.leBaselinePolyGrade.setText(QCoreApplication.translate("Dialog", u"2", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Interpolation method for baseline under peaks:", None))
        self.cbxInterpolationMethod.setItemText(0, QCoreApplication.translate("Dialog", u"Peak-height weight", None))
        self.cbxInterpolationMethod.setItemText(1, QCoreApplication.translate("Dialog", u"Cubic spline", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"Fit strategy", None))
        self.cbxFitStrategy.setItemText(0, QCoreApplication.translate("Dialog", u"Peak fit after baseline subtraction", None))
        self.cbxFitStrategy.setItemText(1, QCoreApplication.translate("Dialog", u"baseline and peak parameters determination in one step", None))

        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Peak identification", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Tolerance:", None))
        self.leToler.setText(QCoreApplication.translate("Dialog", u"0,3", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"keV", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Dialog", u"Analysis Parameters", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Energy X channel parameters", None))
        self.cbxEnChFitType.setItemText(0, QCoreApplication.translate("Dialog", u"Polyn. gr. 2", None))
        self.cbxEnChFitType.setItemText(1, QCoreApplication.translate("Dialog", u"Linear", None))

        self.doEnChFitPbt.setText(QCoreApplication.translate("Dialog", u"Do energy x channel fit", None))
        self.pbtClearEnergyCalibration.setText(QCoreApplication.translate("Dialog", u"Clear energy calibration", None))
        self.pbtAcceptNewEnergies.setText(QCoreApplication.translate("Dialog", u"Accept new energy values", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"FWHM X channel parameters", None))
        self.cbxFwhmChFitType.setItemText(0, QCoreApplication.translate("Dialog", u"a0 + a1 * sqrt(En)", None))
        self.cbxFwhmChFitType.setItemText(1, QCoreApplication.translate("Dialog", u"a0 + a1*En + a2*En^2", None))

        self.doFwhmChFitPbt.setText(QCoreApplication.translate("Dialog", u"Do FWHM x channel fit", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Peak Search", None))
        self.tlBinFiltGr.setText(QCoreApplication.translate("Dialog", u"Binomial filter grade", None))
        self.leBinFiltGr.setText(QCoreApplication.translate("Dialog", u"2", None))
        self.tlPkcut.setText(QCoreApplication.translate("Dialog", u"Search sensitivity", None))
        self.lePkcut.setText(QCoreApplication.translate("Dialog", u"0,3", None))
        self.tlSideChannelsSearch.setText(QCoreApplication.translate("Dialog", u"# of channels on each side:", None))
        self.leSideChannelsSearch.setInputMask("")
        self.leSideChannelsSearch.setText(QCoreApplication.translate("Dialog", u"6", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Data points:", None))
        self.pbtNewSearch.setText(QCoreApplication.translate("Dialog", u"New search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("Dialog", u"Energy Calibration", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Efficiency points - number:", None))
        self.neffptsLne.setText("")
        self.doefficfitPbt.setText(QCoreApplication.translate("Dialog", u"Do fit", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Efficiency X energy parameters - Polynomial grade:", None))
        self.polygradeLne.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("Dialog", u"Efficiency Calibration", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_10), QCoreApplication.translate("Dialog", u"Nuclide Lib.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), QCoreApplication.translate("Dialog", u"Peak Report", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_11), QCoreApplication.translate("Dialog", u"Activities", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), QCoreApplication.translate("Dialog", u"Fit Log", None))
    # retranslateUi

