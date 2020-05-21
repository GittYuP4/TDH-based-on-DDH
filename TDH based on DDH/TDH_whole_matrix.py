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
        Gg = G.g()
        p = G.o
        g = np.array(G.gcycle(p))
        for i in g:
            if i != 1:
                g = i
        #2. Sample a matrix A
        A = getBinaryMatrix(n)
        #3.Create hash key output; Pillar sign means Product from i=1 to n or over all elements i in set I
        hashkey = (Gg,p,g), A
        return hashkey

    #G for generating algorithm takes as inputs a hash key hk and a predicate f element of Fn (predicate) (hk,fi) and outputs a pair of an encoding key ek and trapdoor td
    def generating_algorithm(self,sampling_algorithm):
        #1.s;trapdoor: uniform integer t in Zp
        #g generates group Zp with g**k mod p with values between 1 and p-1 --s,t both element of Zp
        (G,p,g), A = sampling_algorithm
        s = random.choice(G)
        trapdoor = random.choice(G) #TBD: Make t a trapdoor function which output for every key_nr another t_nr
        #2. Set
        #u = g**s
        encoding_key = key_matrix(n,A,s,trapdoor,g)
        key_1 = encoding_key[0][0] #TBD: replace by algorithm choosing random smaller matrix from key-matrix
        key_2 = encoding_key[1][1]
        #3. Output
        #ek = (u,key)
        #td = (s,t)
        return encoding_key,trapdoor
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
        key_nr = generating_algorithm[0]
        e_key_nr = hash_value(key_nr,n) # taken only x parts of key_nr => is that the whole encryption?
        #ê = distance(e_key_nr)%2 #TBD
        #e = u**r * hashkey(key,n)
        return e_key_nr

    #D(td,h) -- Decoding -- The decoding algorithm takes as input a trapdoor td, a hash value h element of {0,1}**n_long
    #...and outputs a pair of a 0-encoding and a 1-necoding (e0,e1) element of {0,1}**w x {0,1}**w
    def decoding_algorithm(self,sampling_algorithm,hashing_algorithm,generating_algorithm,encoding_algorithm):
        (G, p, g), A = sampling_algorithm #imported for the generator needed but it seams as its not the generator meant but the g from matrix key -- as well receiver can't have access to full Matrix A,otherwise would not need encoding
        h = hashing_algorithm
        t = generating_algorithm[1]
        h_t = [element ** t for element in h]
        h_t_g = [element * g for element in h_t]
        e_nr = encoding_algorithm
        x_i = 0
        for i in range(n-1):
            if e_nr[i] == h_t[i]:
                x_i= 0
            if e_nr[i] == h_t_g[i]:
                x_i = 1
        e_0 = h_t
        e_1 = [element **x_i for element in h_t]

        return e_0,e_1

        ##4.2.2.Augmentation to rate-1 TDH in the expense of a λ1 error probability

if __name__ == '__main__':
    lambda_var = 2                  #int(raw_input("Enter lambda value: "))
    n = 10                            #int(raw_input("Enter input length: "))
    sampling_algorithm = TDH(lambda_var,n).sampling_algorithm(lambda_var,n)
    generating_algorithm = TDH(lambda_var,n).generating_algorithm(sampling_algorithm)
    hashing_algorithm = TDH(lambda_var,n).hashing_algorithm(sampling_algorithm,n)
    encoding_algorithm = TDH(lambda_var,n).encoding_algorithm(generating_algorithm,n)
    decoding_algorithm = TDH(lambda_var,n).decoding_algorithm(sampling_algorithm,hashing_algorithm,generating_algorithm,encoding_algorithm)
    print(sampling_algorithm)
    print(decoding_algorithm)