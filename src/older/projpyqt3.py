# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 15:14:45 2016

@author: mmaduar
"""

# projpyqt3 eh o projeto corrente

import sys
from PyQt5.QtGui import QIcon, QKeySequence

from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QVBoxLayout)
from ui_appmainwindow import (Ui_MainWindow)
from rawspectrumdata import (RawSpectrumData)
from parsedspectrumdata import (ParsedSpectrumData)
from spectrumdb import (SpectrumDb)
from countsplot import (MyStaticMplCanvas)

import sdi_rc

class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.openAct = QAction(QIcon(':/images/open.png'), "&Open...", self,
        # shortcut=QKeySequence.Open, statusTip="Open an existing file",
        # triggered=self.open)
        self.ui.action_Open.triggered.connect(self.slotOpen)
        # 2017-03-24 AQUI acionando o menu exit
        self.ui.actionE_xit.triggered.connect(self.slotExit)
    
        self.verticalLayout_2 = QVBoxLayout(self.ui.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.docum = RawSpectrumData()
        # AQUI talvez precise setar vinculo com o container
        self.docum.setObjectName("docum")
        self.verticalLayout_2.addWidget(self.docum)

        self.l3 = QVBoxLayout(self.ui.tab_3)
        self.l3.setObjectName("l3")
        # self.specplot = CountsPlot()
        # AQUI talvez precise setar vinculo com o container
        # self.specplot.setObjectName("specplot")
        # self.verticalLayout_3.addWidget(self.specplot)
        
        self.sc = MyStaticMplCanvas(self.ui.tab_3, width=5, height=4, dpi=100)
        self.l3.addWidget(self.sc)
        
        # 2017-03-29 Plot #2 em scPlot2 (matplotlib static canvas)
        self.l4 = QVBoxLayout(self.ui.tab_4)
        self.l4.setObjectName("l4")
        self.scPlot2 = MyStaticMplCanvas(self.ui.tab_4, width=5, height=4, dpi=100)
        self.l4.addWidget(self.scPlot2)
      
        # 2017-03-29 Plot #3 em scPlot3(matplotlib static canvas)
        self.l5 = QVBoxLayout(self.ui.tab_5)
        self.l5.setObjectName("l5")
        self.scPlot3 = MyStaticMplCanvas(self.ui.tab_5, width=5, height=4, dpi=100)
        self.l5.addWidget(self.scPlot3)
        
        self.parsed = ParsedSpectrumData()
        
        # self.main_widget.setFocus()
        # self.setCentralWidget(self.main_widget)

        # self.statusBar().showMessage("All hail matplotlib!", 2000)

    def slotOpen(self):
#       fileName, _ = QFileDialog.getOpenFileName(self)
        fileName, _ = QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()", "~/wolkesicher/ipen/Genie2k/Camfiles/ALMERA",
                "IEC spectra (*.IEC);;Text Files (*.iec)" )
        if fileName:
            if self.docum.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                # 2017-04-29 Create db for this spectrum
                self.uiuiui = SpectrumDb(fileName + '.db')
                self.parsed.readiecsp( fileName )
                print( self.parsed.lt )

                self.parsed.analyzeiecsp()

                self.sc.plotnewdata(self.parsed.nonull_chan, self.parsed.nonull_cnts,
                                    self.parsed.nonull_unct )

                print(self.parsed.regions, self.parsed.xforplot, self.parsed.bl_forplot, self.parsed.net_forplot)


                self.scPlot2.plotwstd( self.parsed.wstd )
                self.sc.plotRegionsFit( self.parsed.regions, self.parsed.zrg )
                self.sc.plotBaselinesFit( self.parsed.zbl, self.parsed.blin )
                # self.sc.plotOtherStuff( self.parsed.regions, self.parsed.xforplot,
                #                       self.parsed.bl_forplot, self.parsed.net_forplot)
    # 2017-03-24 AQUI definindo o slot exit
    def slotExit(self):
        QApplication.instance().closeAllWindows()
    
if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    else:
        print('jah egziste!!! : %s' % str(app))

    mainWin = AppWindow()
    mainWin.show()
    
    # http://stackoverflow.com/questions/25007104/what-the-error-when-i-close-the-dialog
    # 2017-03-27  AQUI para usar a partir do IPython (interative prompt)
    app.exec_()
    # 2017-03-27  e AQUI para usar a chamada direta 
    # sys.exit(app.exec_()) 
