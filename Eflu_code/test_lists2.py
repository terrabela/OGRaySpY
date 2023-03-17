# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 17:47:35 2016

@author: marcelo
"""
import numpy as np
import matplotlib.pyplot as plt

def comparer(a1, a2, i1, i2, maxgap):
    return abs(a1[i1] - a2[i2]) <= maxgap

def plotlins(lins, codcolor):
    for ili in range(len(lins)):
        ptsinline = [[xs[ipt] for ipt in lins[ili]],
                     [ ys[ipt] for ipt in lins[ili]]]
        plt.plot( ptsinline[0], ptsinline[1], color=codcolor,
                 linewidth=0.5, ls='-')

a1 = [np.random.randint(1000) for i1 in range(17)]
a2 = [np.random.randint(1000) for i1 in range(17)]

li1 = [np.random.randint(17) for i1 in range(7)]
li2 = [np.random.randint(17) for i1 in range(7)]

seq1 = [ a1[i] for i in li1 ]
seq2 = [ a2[i] for i in li2 ]

compar = comparer(a1, a2, li1[0], li2[4], 100)
compars1 = [ comparer(a1, a2, i1, i2, 100)
             for i1 in li1 for i2 in li2 if i1<i2]
compars2 = [ comparer(a1, a2, i1, i2, 100)
             for i1 in li1 for i2 in li2 if i1<i2]

xs = []
ys = []

for ipt in range(100):
    xs.append( np.random.randint( 1000 ) )
    ys.append( np.random.randint( 1000 ) )
# propriedade da linha
# plt.setp( lines, color='r' )

plt.figure(1)
# plt.subplot(111)
plt.plot( xs, ys, 'g^', fillstyle='none')

# teste com linhas constru´idas aleatoriamente com pontos em xs, ys
nlins = 7
lins = []
lins2 = []

for ili in range(nlins):
    npt = np.random.randint( 5 ) 
    lins.append([])
    lins2.append([])
    for ipt in range(npt):
        lins [ili].append( np.random.randint(100) )
        lins2[ili].append( np.random.randint(100) )

# plotlins(lins, 'r')
# plotlins(lins2, 'b')

# teste com linhas constru´idas entre pontos pr´oximos de xs, ys

lins3 = []
for ipt in range(100):
    for jpt in range(ipt):
        if comparer(xs, xs, ipt, jpt, 37) and \
        comparer(ys, ys, ipt, jpt, 37):
            lins3.append([ipt, jpt])

plotlins(lins3, 'b')

plt.show()
