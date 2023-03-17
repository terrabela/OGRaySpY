#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 15:20:12 2022

@author: maduar
"""

def AA(matX, k, tmaxouter=100, tmaxinner=100, tol=0.0001):
    # determine size of matrix X
    m, n = matX.shape

    # pre-compute Gram matrix X’X
    matXtX = np.dot(matX.T, matX)

    # random initialization of matrix A of archetypes
    matA = matX[:,rnd.choice(n, k, replace=False)]

    # dummy initialization of coefficient matrices Y and Z
    matY = np.zeros((n,k)); matY[0] = 1.
    matZ = np.zeros((k,n)); matZ[0] = 1.

    # initialize error value
    E_old = np.inf

    # iteratively update matrices Z and Y
    for t in range(tmaxouter):
        # given A, update Z using FW
        matAtA = np.dot(matA.T, matA)
        matAtX = np.dot(matA.T, matX)
        matZ = fwUpdateZ(matAtA, matAtX, matZ, tmaxinner)

        # given Z, update Y using FW
        matZZt = np.dot(matZ, matZ.T)
        matXtXZt = np.dot(matXtX, matZ.T)
        matY = fwUpdateY(matXtX, matXtXZt, matZZt, matY, tmaxinner)

        # given Y, update A
        matA = np.dot(matX, matY)

        # compute current error
        E_new = la.norm(matX - np.dot(matA, matZ))

        # terminate loop if error did not improve much
        if np.abs(E_old - E_new) < tol:
            break
        else:
            E_old = E_new

    # perform final update of Z
    matAtA = np.dot(matA.T, matA)
    matAtX = np.dot(matA.T, matX)
    matZ = fwUpdateZ(matAtA, matAtX, matZ, tmaxinner)
    return matA, matY, matZ
    
def fwUpdateZ(AtA, AtX, Z, tmax=100):
    k, n = Z.shape
    inds = np.arange(n)

    for t in range(tmax):
        beta = 2. / (t+2)
        grad = np.dot(AtA, Z) - AtX

        imin = np.argmin(grad, axis=0)

        Z *= (1-beta)
        Z[imin,inds] += beta

    return Z


def fwUpdateY(XtX, XtXZt, ZZt, Y, tmax=100):
    n, k = Y.shape
    inds = np.arange(k)

    for t in range(tmax):
        beta = 2. / (t+2)
        grad = np.dot(np.dot(XtX, Y), ZZt) - XtXZt

        imin = np.argmin(grad, axis=0)

        Y *= (1-beta)
        Y[imin,inds] += beta

    return Y
