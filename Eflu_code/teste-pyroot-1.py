# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:48:39 2014

@author: marcelo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:50:03 2014

@author: marcelo
"""

# Example: displaying a ROOT histogram from Python
from ROOT import gRandom,TCanvas,TH1F

c1 = TCanvas('c1','Example',200,10,700,500)
hpx = TH1F('hpx','px',100,-4,4)

for i in xrange(25000):
    px = gRandom.Gaus()
    hpx.Fill(px)
    
hpx.Draw()
c1.Update()