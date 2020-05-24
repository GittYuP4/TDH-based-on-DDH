from __future__ import generators
from random import randint
import random
import numpy as np
import hashlib

#https://stackoverflow.com/questions/27784465/how-to-randomly-get-0-or-1-every-time

#generate random public parameters with values {0,1} and put into binary matrix A
def getRandomMatrix(n):
    #matrix = np.array([[str(randint(0, 1)) for _ in range(0, n)] for _ in range(0, 2)]).astype(np.int8)
    matrix = np.random.randint(2, size=(2, n))
    return matrix

def hash_value_paper(A,p,g,n):
    hash = 0
    for i in range(2):
        for j in range(10):
            hash = p*hash + A[i][j]    #https://math.stackexchange.com/questions/188003/hash-function-for-matrices-over-finite-field-matlab
    return hash

#https://www.geeksforgeeks.org/sha-in-python/ -- SHA, ( Secure Hash Algorithms )
#The variety of SHA-2 hashes can lead to a bit of confusion, as websites and authors express them differently.
#If you see “SHA-2,” “SHA-256” or “SHA-256 bit,” those names are referring to the same thing. If you see “SHA-224,” “SHA-384,” or “SHA-512,” those are referring to the alternate bit-lengths of SHA-2.
def sha256_hash(A):
    A = str(A)
    result = hashlib.sha1(A.encode()) #This hash function belong to hash class SHA-2, the internal block size of it is 32 bits.
    return result.hexdigest()


def hash_value_yt(A,n):
    #works
    hash = []
    y=0
    while y != n-1:
            if A[0][y] == 0:
               hash.append(0)
            if A[1][y] == 1:
               hash.append(1)
            y += 1
    return hash

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
