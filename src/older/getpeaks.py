# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:15:36 2014

@author: marcelo
"""

from ROOT import TH1F, TH1, TSpectrum, TFile
from pprint import pformat
 
def get_gpeaks(h,lrange=[1000,3800],sigma=2,opt="",thres=0.05,niter=20):
    s = TSpectrum(niter)
    h.GetXaxis().SetRange(lrange[0],lrange[1])
    s.Search(h,sigma,opt,thres)
    bufX, bufY = s.GetPositionX(), s.GetPositionY()
    pos = []
    for i in range(s.GetNPeaks()):
        pos.append([bufX[i], bufY[i]])
    pos.sort()
    return pos
 
def get_all_he(f):
    f.Get("histos").ls()
    hs = []
    for i in range(16):
        hs.append( f.Get("RADC0_%02d"%i) )
    return hs
 
def get_all_peaks_info(f):
    histos = get_all_he(f)
    pchs = []
    for i in [0,1,2,3,12,13,14,15]:
        info = '"' + histos[i].GetName() + '":'
        info += pformat(get_gpeaks(histos[i]))
        pchs.append(info)
    return pchs
 
def info_write2json(fr, fj):
    fdat = TFile(fr)
    fout = open(fj,"w")
    pinfo = get_all_peaks_info(fdat)
    fout.write("{\n")
    for i in pinfo[:-1]: fout.write(i+",\n")
    fout.write(pinfo[-1])
    fout.write("\n}\n")
    fout.close()
 
if __name__=="__main__":
    print "Usage: getgpeaks.py <file.root>"