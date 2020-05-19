import numpy as np
import random
import matplotlib.pyplot
from pip._vendor.distlib.compat import raw_input
from TDH_functions import *

from groups import Group #https://github.com/Smeths/pygroup

#Goal: Implement the Trapdoor hash function from DDH assumption

class TDH(object):
    #4.2. TDH for Index Predicates from DDH
    ##4.2.1“basic” construction of a rate-1/λ TDH scheme for index predicates
    def __init__(self,lambda_var,n):
        self.lambda_var = lambda_var
        self.n = n

    #S for Sampling Algorithm with inputs security parameter lambda and input length n (1^lambda,1^n)
    #..and outputing as hash key hk
    def sampling_algorithm(self,lambda_var,n):
        #1. Sample (G; p; g); (Finite-) multiplicative abelian group G of prime order p, with a public generator g
        G = Group("mult", 15)
        p = G.o
        g = np.array(G.gcycle(p))
        for i in g:
            if i != 1:
                g = i
        #2. Sample a matrix A
        A = getBinaryMatrix(n)
        #3.Create hash key output; Pillar sign means Product from i=1 to n or over all elements i in set I
        return (G,p,g),A

    #G for generating algorithm takes as inputs a hash key hk and a predicate f element of Fn (predicate) (hk,fi) and outputs a pair of an encoding key ek and trapdoor td
    def generating_algorithm(self,sampling_algorithm):
        #1.s;trapdoor: uniform integer t in Zp
        #g generates group Zp with g**k mod p with values between 1 and p-1 --s,t both element of Zp
        (G,p,g), A = sampling_algorithm
        s = random.choice(G.g())
        t = random.choice(G.g())
        #2. Set
        #u = g**s
        key = key_matrix(n,A,s,t,g)
        print(key_matrix(n,A,s,t,g))
        #3. Output
        #ek = (u,key)
        #td = (s,t)
        return key,t
    #H for Hashing algorithm taking hash key hk, a string x element of {0,1}**n as well as randomness p_dense element of {0,1}* as input.
    #... and deterministically outputs a hash value h element of {0,1}**n_long
    def hashing_algorithm(self,sampling_algorithm,n):
        (G,p,g), A = sampling_algorithm
        h = hash_value(A, n)
        #r = random.choice(G.g())
        #h = (g**r) * A
        return h

    #E(ek,x;p) -- Hinting -- The encoding algorithm takes as input an encoding key ek, string x element of {0,1}**n as well as randomness p_dense elemnt of {0,1}* as input.
    #..and deterministically outputs an encoding e element of {0,1}**w.
    def encoding_algorithm(self,generating_algorithm,n):
        key = generating_algorithm[0]
        e = hash_value(key,n)
        #e = u**r * hashkey(key,n)
        return e

    #D(td,h) -- Decoding -- The decoding algorithm takes as input a trapdoor td, a hash value h element of {0,1}**n_long
    #...and outputs a pair of a 0-encoding and a 1-necoding (e0,e1) element of {0,1}**w x {0,1}**w
    def decoding_algorithm(self,sampling_algorithm,generating_algorithm,encoding_algorithm):
        (G, p, g), A = sampling_algorithm
        h = generating_algorithm[0]
        t = generating_algorithm[1]
        e = encoding_algorithm
        for i in e:
            if i == 0:
                e[i] = h**t
            if i == 1:
                e[i] = (h**t) * g
        return e

        ##4.2.2.Augmentation to rate-1 TDH in the expense of a λ1 error probability

if __name__ == '__main__':
    lambda_var = int(raw_input("Enter lambda value: "))
    n = int(raw_input("Enter input length: "))
    sampling_algorithm =  TDH(lambda_var,n).sampling_algorithm(lambda_var,n)
    generating_algorithm = TDH(lambda_var,n).generating_algorithm(sampling_algorithm)
    hashing_algorithm = TDH(lambda_var,n).hashing_algorithm(sampling_algorithm,n)
    encoding_algorithm = TDH(lambda_var,n).encoding_algorithm(generating_algorithm,n)
    decoding_algorithm = TDH(lambda_var,n).decoding_algorithm(sampling_algorithm,generating_algorithm,encoding_algorithm)
    print(TDH.sampling_algorithm)
    print(TDH.decoding_algorithm)