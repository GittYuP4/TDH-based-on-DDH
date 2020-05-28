from __future__ import generators
from random import randint
import random
import numpy as np
import hashlib
import math
from scipy.stats import logser
import sys
SEED_SIZE  = 16
GENERATOR  = 223
MODULUS    = 36389
FUNCTION_L = lambda x: x**2 - 2*x + 1

#https://stackoverflow.com/questions/27784465/how-to-randomly-get-0-or-1-every-time

#generate random public parameters with values {0,1} and put into binary matrix A
def getRandomMatrix(n):
    matrix = np.array([[str(randint(0, 1)) for _ in range(0, n)] for _ in range(0, 2)]).astype(np.int8)
    #matrix = np.random.randint(2, size=(2, n))
    return matrix

def hash_value_paper(A,g,r,n):
    hash = np.longdouble(1)
    g_r = g**r
    for i in range(2):
        for j in range(n):
            #hash = g_r*hash + A[i][j]    #https://math.stackexchange.com/questions/188003/hash-function-for-matrices-over-finite-field-matlab
            hash = hash*A[i][j]
    hash = g_r*hash
    return hash

#https://www.geeksforgeeks.org/sha-in-python/ -- SHA, ( Secure Hash Algorithms )
#The variety of SHA-2 hashes can lead to a bit of confusion, as websites and authors express them differently.
#If you see “SHA-2,” “SHA-256” or “SHA-256 bit,” those names are referring to the same thing. If you see “SHA-224,” “SHA-384,” or “SHA-512,” those are referring to the alternate bit-lengths of SHA-2.
def sha256_hash(A):
    A = str(A)
    result = hashlib.sha1(A.encode()) #This hash function belong to hash class SHA-2, the internal block size of it is 32 bits.
    return result.hexdigest()

def hash_value_yt(A,g,r,n):
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
    key_matrix = np.zeros((2,n),dtype=np.longdouble)
    rows = 2
    columns = n
    for i in range(rows):
        for j in range(columns):
            if j == ii and i==1:
                key_matrix[1][j] += ((A[1][ii])**s)*(g**t)
            else:
                key_matrix[i][j] += (A[i][j])**s
    return key_matrix

def distance_g_t_paper(e,delta,M,K,g,t):
    T = (2*M*math.log(2/delta))/delta
    LSB = 0 #least significant bit, gibt Parität an eines bit-strings,d.h. ob gerade(1) oder ungerade(0)
    i=0
    g_t = g**t
    random.seed()
    log_2M = []
    upper_bound = int(round(math.log(2*M/delta), 0))
    #PRF_K_i = []  #(e*(g_t)) #e is the hash values
    for x in range(upper_bound):
        log_2M.append(0)
        #PRF_K_i.append(random.randint(0,1))
    while i <= T:
        #PRF_K_i = [element ** i for element in PRF_K_i]
        PRF_K_hgi = random.choices(K,e*(g**i))
        if np.array_equal(PRF_K_hgi,log_2M):
            LSB = i
            return LSB
        i +=1

def distance_g_t_yt(e,delta,M,K):
    T = (2*M*math.log(2/delta))/delta
    LSB = 0 #longest string bit
    i=0
    dlog = logser.logpmf(K,delta)
    while i <= T:
        if logser.ppf(i, 1, len(K)) == 0**(round(M*math.log(2/delta),1)):
            LSB = i
            return LSB
        i +=1


def function_H(first_half, second_half):
    mod_exp = bin(pow(GENERATOR, int(first_half, 2), MODULUS)).replace('0b', '').zfill(SEED_SIZE)
    hard_core_bit = 0
    for i in range(len(first_half)):
        hard_core_bit = (hard_core_bit ^ (int(first_half[i]) & int(second_half[i]))) % 2
    return mod_exp + second_half + str(hard_core_bit)

#https://towardsdatascience.com/building-a-pseudorandom-number-generator-9bc37d3a87d5
def function_G(e,delta,M,K,g,t):
    binary_string = K
    result = ''
    for i in range(FUNCTION_L(SEED_SIZE)):
        first_half = binary_string[:len(binary_string)/2]
        second_half = binary_string[len(binary_string)/2:]
        binary_string = function_H(first_half, second_half)
        result += binary_string[-1]
        binary_string = binary_string[:-1]
    return result