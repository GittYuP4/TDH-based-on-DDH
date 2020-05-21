from __future__ import generators
from random import randint
import random
import numpy as np

#https://stackoverflow.com/questions/27784465/how-to-randomly-get-0-or-1-every-time

#generate random public parameters with values {0,1} and put into binary matrix A
def getRandomMatrix(n):
    #matrix = np.array([[str(randint(0, 1)) for _ in range(0, n)] for _ in range(0, 2)]).astype(np.int8)
    matrix = np.random.randint(2, size=(2, n))
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
    ii = random.randint(0,n-1) #ii, meaning i, remains private given the encoding key
    key_matrix = A
    rows = 2
    columns = n
    for i in range(rows):
        for j in range(columns):
            if j == ii and i==1:
                key_matrix[1][j] = ((key_matrix[1][ii])**s)*(g**t)
            else:
                key_matrix[i][j] = (key_matrix[i][j])**s
    return key_matrix
