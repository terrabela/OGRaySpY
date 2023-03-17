# -*- coding: utf-8 -*-
"""
@author: mmaduar
"""

# 2017-07-19
# ogmwdcaller eh o main file doprojeto corrente

import sys
from PyQt5 import QtWidgets
from ogmwd import (OpenGammaMainWindow)

if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    else:
        print('jah egziste!!! : %s' % str(app))
       
    MainWindow = OpenGammaMainWindow()
    MainWindow.show()

    # http://stackoverflow.com/questions/25007104/what-the-error-when-i-close-the-dialog
    # 2017-03-27  AQUI para usar a partir do IPython (interative prompt)
    app.exec_()
    # 2017-03-27  e AQUI para usar a chamada direta 
    # sys.exit(app.exec_()) 
