from __future__ import generators
from random import randint
import random
import numpy as np

#https://stackoverflow.com/questions/27784465/how-to-randomly-get-0-or-1-every-time

#generate random public parameters with values {0,1} and put into matrix A
def getBinaryMatrix(n):
    matrix = np.array([[str(randint(0, 1)) for _ in range(0, n)] for _ in range(0, 2)]).astype(np.int8)
    #for row in matrix:
     #   print("".join(row))

    return matrix

def hash_value(A,n):
    #hk = np.prod(A)
    hk = []
    y=0
    while y != n-1:
            if A[0][y] == 0:
               hk.append(0)
            if A[1][y] == 1:
               hk.append(1)
            y += 1

    return hk

def key_matrix(n,A,s,t,g):
    i = random.randint(0,n-1)            #i remains private given the encoding key
    #matrix = np.ones((2,n),np.int8)
    for row in A-1:
        for col in range(0,n-1):
            if A[1][i]:
                A[1][col] = ((A[1][col])**t)*g
            else:
                A[row][col] = (A[row][col])**t
    return A