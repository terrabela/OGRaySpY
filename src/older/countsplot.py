# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 22:50:36 2016

@author: Marcelo
"""

#!/usr/bin/env python

# Fonte:
# http://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html

# embedding_in_qt5.py --- Simple Qt5 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#               2015 Jens H Nielsen
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

from __future__ import unicode_literals
import sys
import os
import random
# import matplotlib
# Make sure that we are using QT5
# matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as MplToolbar

from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.autoscale()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # self.mpltb = MplToolbar(parent=self, canvas=self)
        # ou, sem nomear os parametros:
        self.mpltb = MplToolbar(self, self)


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a spectrum plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.counts = []

    def plotnewdata( self, xplot, yplot, syplot ):
        
        # 2017-03-28 Study this:
        # http://www.python-course.eu/python3_properties.php
        
        # decorating x- and y- axes
        self.axes.set_xlabel('channel')
        self.axes.set_ylabel('counts')
        
        #  calls helper methods to create graphics primitives
        # spect_envelope, = self.axes.plot( self.counts, linewidth=0.2 )
        # counts_dots, = self.axes.plot( self.xplot, self.yplot, 'bo', markersize=0.5 )
        # uncert_dots, = self.axes.plot( self.xplot, self.syplot, 'ro', markersize=0.3 )
        # counts_dots, = self.axes.errorbar( x=self.xplot, y=self.yplot, yerr=self.syplot,
        #                                  fmt='bo', markersize=1.0, ecolor='m',
        #                                  elinewidth=0.2, capsize=1.0 )
        self.axes.errorbar(x=xplot, y=yplot, yerr=syplot, ecolor='cyan',
                           elinewidth=0.5, capsize=2, antialiased=True, fmt='none')
        self.axes.plot(xplot, yplot, 'D', ms=2, mfc='yellow', mec='blue', mew=0.5,
                       antialiased=True )
        
        # test remotion
        # self.axes.lines.remove( uncert_dots )
        
        self.draw_idle()
        
    def plotwstd( self, wstd ):
        self.wstd = wstd
        self.axes.plot( self.wstd, label='sd/sqrt(mean)', linewidth=0.3 )
        self.draw_idle()
        
    # AQUI 2017-03-28    
    # def plotanalysisresults( self, ... )
    
    # plot regions fit
    def plotRegionsFit( self, regions, zrg ):
        print ('regions: ', regions)
        print ('zrg: ', zrg)
        for i in range(len(regions)):
            xp = np.linspace(regions[i][0], regions[i][1], 50)
            # 2016-06-30: PAREI AQUI agora tem que fazer o ajuste gaussiano
            # so' coloquei polinomial para testar
            p = np.poly1d( zrg[i] )
            self.axes.plot( xp, p(xp), color='Plum', linewidth=1.3 )
            
    # plot baselines fit
    def plotBaselinesFit( self, zbl, blin ):
        for i in range(len(zbl)):
            print('Baseline fit: ', i)    
            xp = np.linspace(blin[i][0], blin[i][1], 50)
            p = np.poly1d( zbl[i] )
            self.axes.plot( xp, p(xp), color='Orange', linewidth=1.0)
            
    def plotOtherStuff( self, regions, xforplot, bl_forplot, net_forplot ):
        print ('regions: ', regions)
        print ('xforplot: ', xforplot)
        print ('bl_forplot: ', bl_forplot)
        print ('net_forplot: ', net_forplot)
        for i in range(len(regions)):
            self.axes.plot( xforplot, bl_forplot, color='OrangeRed', linewidth=1.0)
            self.axes.plot( xforplot, net_forplot, color='Cyan', linewidth=1.0)

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()
