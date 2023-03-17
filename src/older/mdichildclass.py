# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:41:17 2016

@author: marcelo
"""

from PyQt4 import QtCore, QtGui

class MdiChild(QtGui.QTextEdit):
    sequenceNumber = 1

    def __init__(self):
        super(MdiChild, self).__init__()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True

    #2016:
    def processiecspectrum(self, origstring ):
        # instr2 = QtCore.QTextStream( origstring )
        blocknumlines = 1,  1,  1,  1, 1,  4, 1,  12,  12,  12,  12
        descriptors = (
            "foo1(text) det(text) n1 n2 n3", 
            "foo2(text) lt rt nchan", 
            "dateacq(text) timeacq(text)", 
            "foo3(text) a1 a2 a3 a4", 
            "foo4(text) b1 b2 b3 b4 b5 b6", 
            "foo5(text) sampid1(text) sampid2(text) sampid3(text) sampid4(text) sampid5(text) sampid6(text) sampid7(text) sampid8(text) sampid9(text)", 
            "foo6(text)", 
            "foo7(text) en1 en2 en3 en4", 
            "foo8(text) a1 b1 c1 d1", 
            "foo9(text) e1 f1 g1 h1", 
            "fooa(text)", 
            "foob(text) ch counts[1:5]"
            )
        
        idesc = 0
        resultstring = ""
        
        # for ibl in blocknumlines:
        #    resultstring += "descriptor "
        #    resultstring += descriptors[idesc]
        #    idesc += 1
        #    resultstring += "\n"
        #    for i in range( ibl ):
        #        resultstring += origstring.. instr2.readLine() + "\n"  AQUI 2016-02-03
        #        resultstring += "\n"
        lines = origstring.splitlines()
         
        resultstring += "descriptor "
        resultstring += descriptors[idesc]
        resultstring += "\n"
        # resultstring += instr2.readAll()  AQUI 2016-02-03
        return lines
        
    def newFile(self):
        self.isUntitled = True
        self.curFile = "document%d.txt" % MdiChild.sequenceNumber
        MdiChild.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

        self.document().contentsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "OpenGRay",
                "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False
        instr = QtCore.QTextStream(file)
         
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.setPlainText(instr.readAll())
        self.setCurrentFile(fileName)
        self.document().contentsChanged.connect(self.documentWasModified)

        str1 = instr.readAll()
        str2 = ""
        # str2 = self.processiecspectrum( str1 )
        # self.dialog1.setTextBoxes( str2 )
        strlines = self.processiecspectrum( str1 )
        ili = 0
        for li in strlines:
            ili += 1
            self.append( li )
        self.append( )
        QtGui.QApplication.restoreOverrideCursor()
        return True

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save As",
                self.curFile)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "MDI",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outstr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outstr << self.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        return True

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.document().isModified())

    def maybeSave(self):
        if self.document().isModified():
            ret = QtGui.QMessageBox.warning(self, "MDI",
                    "'%s' has been modified.\nDo you want to save your "
                    "changes?" % self.userFriendlyCurrentFile(),
                    QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                    QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False

        return True

    def setCurrentFile(self, fileName):
        self.curFile = QtCore.QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()
