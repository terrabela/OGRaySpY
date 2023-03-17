# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 17:14:01 2014

@author: marcelo
"""

from ROOT import gROOT, TCanvas, TF1
 
gROOT.Reset()
c1 = TCanvas( 'c1', 'Example with Formula', 200, 10, 700, 500 )
 
#
# Create a one dimensional function and draw it
#
fun1 = TF1( 'fun1', 'abs(sin(x)/x)', 0, 10 )
c1.SetGridx()
c1.SetGridy()
fun1.Draw()
c1.Update()
