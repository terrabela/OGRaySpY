# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:31:09 2014

@author: marcelo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:50:03 2014

@author: marcelo
"""

# Example: displaying a ROOT histogram from Python
import ROOT

def roothistogram():
    c1 = ROOT.TCanvas('c1','Example',200,10,700,500)
    hpx = ROOT.TH1F('hpx','px',100,-4,4)
    for i in xrange(25000):
        px = ROOT.gRandom.Gaus()
        hpx.Fill(px)
    hpx.Draw()
    c1.Update()
    return 0
