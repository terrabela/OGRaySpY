# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 17:47:35 2016

@author: marcelo
"""
import numpy as np
import matplotlib.pyplot as plt

def buildlins( lins, pts ):
    nlins = len(lins)
    xs = [ pt[0] for pt in pts ]
    ys = [ pt[1] for pt in pts ]
    for ili in range(nlins):
        ptsinline = [[xs[ipt] for ipt in lins[ili]], [ ys[ipt] for ipt in lins[ili]]]
        # plt.plot( ptsinline[0], ptsinline[1], linewidth=0.2, ls='-')
        return ptsinline

plt.figure(1, figsize=(12,8))
pontos1 = plt.plot([1,20,300,400], [100,400,900,160], 'ro')
# plt.axis([0, 6, 0, 20])
# plt.show()

# evenly sampled time at 200ms intervals
plt.figure(figsize=(12,8))
t = np.arange(0., 5., 0.2)
# red dashes, blue squares and green triangles
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.show()

# plt.figure(figsize=(12,8))

xs = []
ys = []

for ipt in range(100):
    xs.append( np.random.randint( 1000 ) )
    ys.append( np.random.randint( 1000 ) )
# propriedade da linha
# plt.setp( lines, color='r' )

plt.figure(1)
# plt.subplot(111)
plt.plot( xs, ys, 'g^')
# plt.plot( xs, ys, linewidth=0.2, ls='-' )

nlins = 7
lins = []
for ili in range(nlins):
    npt = np.random.randint( 5 ) 
    lins.append([])
    for ipt in range(npt):
        lins[ili].append( np.random.randint(100) )

for ili in range(nlins):
    ptsinline = [[xs[ipt] for ipt in lins[ili]], [ ys[ipt] for ipt in lins[ili]]]
    plt.plot( ptsinline[0], ptsinline[1], linewidth=0.2, ls='-')

plt.show()
