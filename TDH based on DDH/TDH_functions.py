from __future__ import generators
import random
import numpy as np
import math

#calculate hash_value with equation 4.5
def hash_value_paper(A,g,r,n):
    hash = np.longdouble(1)
    g_r = g**r
    for i in range(2):
        for j in range(n):
            #hash = g_r*hash + A[i][j]    #https://math.stackexchange.com/questions/188003/hash-function-for-matrices-over-finite-field-matlab
            hash = hash*A[i][j]
    hash = g_r*hash
    return hash

#calculate the encoding matrix with equation 4.6
def key_matrix(n,A,s,t,g):
    ii = random.randint(0,n-1) #ii, meaning index i from the paper
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

#*************************************************************
# Title: prng.py - Building a Pseudorandom Number Generator
# Author: David Bertoldi - firaja
# Date: 2019
# Code version: 1.0
# Availability: https://gist.github.com/firaja/f2eabc05db3fdd4cf60373f5971b4eb3
#*************************************************************
# PRNG functions G and H from prng repo combined with the distance function from chapter 4.2.2
FUNCTION_L = lambda x: x**2 - 2*x + 1
def function_G(h,K,generator,modulus,M,delta):
    T = int((2 * M * math.log(2 / delta)) / delta)
    binary_string = [] #must be even to split string into 2 halfes
    h = int(h)
    generator = int(generator)
    modulus = int(modulus)
    random.seed()
    j = 0
    for j in range(0,K):
        binary_string.append(random.randint(0,1))
        j=j
    binary_string = str("".join(str(i) for i in binary_string))
    result = ''
    for i in range(FUNCTION_L(T)):
        if i == j:
            return result[-1]
        else:
            first_half = binary_string[:int(K/2)]
            second_half = binary_string[int(K/2):]
            binary_string = function_H(first_half, second_half,(h*(generator**i)),T,modulus)
            result += binary_string[-1]
            binary_string = binary_string[:-1]
    return result[-1]

def function_H(first_half, second_half,generator,T,modulus): #helper_PRNG
    mod_exp = bin(pow(generator, int(first_half, 2), modulus)).replace('0b', '').zfill(T) #if we set the modulus higher, we also get a more variation in the result
    hard_core_bit = 0
    for i in range(len(first_half)):
        hard_core_bit = (hard_core_bit ^ (int(first_half[i]) & int(second_half[i]))) % 2
    return mod_exp + second_half + str(hard_core_bit)


