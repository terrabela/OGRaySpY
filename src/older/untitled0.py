# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 17:11:48 2015

@author: usuario
"""

# import PyQt4.QtCore

x = 82
x += 7
print(x)
d = 7
e = d
d = 23
d = "Aiai"
x = 5
y = x
y += 1
print ((x, y))

p = 5 ** 35
print(p)
print(47 % 6)
q = 5.7
r = 8.9e-4
c = 1.2 + 3.45j
print( type(c) )
import random
xra = random.randint(1, 3) #1, 2 ou 3

aa1 = 'Marcelo Francis'
aa1n = len(aa1)
aa2 = aa1[:3]
aa3 = aa1[3:]
aa4 = aa1[:-2]
aa5 = aa1[-2:]
aa6 = aa1[2:9]

def fib(n,zz=0):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    return b
    
def soma(a, b):
    return a+b

def aplic(a, b, c=7):
    return a(b,c)
    
aq1 = aplic(fib, 200)
aq2 = aplic(soma, 7, 5)
print(aq1)
print(aq2)
