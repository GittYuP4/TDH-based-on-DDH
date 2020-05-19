from __future__ import generators
from random import randint
import random
import numpy as np

#https://stackoverflow.com/questions/27784465/how-to-randomly-get-0-or-1-every-time

# Sieve of Eratosthenes to generate primes (if needed)
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/

def getBinaryMatrix(n):
    matrix = np.array([[str(randint(0, 1)) for _ in range(0, n)] for _ in range(0, 2)]).astype(np.int8)
    #for row in matrix:
     #   print("".join(row))

    return matrix

def hashkey(A,n):
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
    matrix = np.ones((2,n),np.int8)
    for row in matrix:
        for col in range(0,n-1):
            if matrix[1][i]:
               matrix[1][col] = ((A[1][col])**s)*(g**t)
            else:
                matrix[row][col] = (A[row][col])**s
    return matrix