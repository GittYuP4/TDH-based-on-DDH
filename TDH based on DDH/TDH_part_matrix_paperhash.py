import numpy as np
import random
from pip._vendor.distlib.compat import raw_input
from TDH_functions import *
from groups import Group #https://github.com/Smeths/pygroup
import hashlib

#Goal: Implement the Trapdoor hash function from DDH assumption

#Encoding working without variation and yt hash function

class TDH(object):
    #4.2. TDH for Index Predicates from DDH
    ##4.2.1“basic” construction of a rate-1/λ TDH scheme for index predicates
    def __init__(self,lambda_var,n):
        self.lambda_var = lambda_var
        self.n = n

    #S for Sampling Algorithm with inputs security parameter lambda and input length n (1^lambda,1^n)
    #..and outputing as hash key hk
    def sampling_algorithm(self,lambda_var,n): # done by the sender, output also private and only used in the hashing_algorithm again by the sender
        #1. Sample (G; p; g); (Finite-) multiplicative abelian group G of prime order p, with a public generator g
        G = Group("mult", 9)
        Gg = G.g() #Group representation
        p = G.o #order of G
        generators_of_G = []
        for i in Gg: #finding generator of Group G
            x = np.array(G.gcycle(i))
            x_sorted = np.sort(x)
            if np.array_equal(Gg,x_sorted):
                generators_of_G.append(i)
        generator = random.choice(generators_of_G)
        rand_elem_1 = np.array(np.random.choice(p, 10), dtype=np.longdouble)
        rand_elem_2 = np.array(np.random.choice(p, 10), dtype=np.longdouble)
        A = np.concatenate(([rand_elem_1], [rand_elem_2]))
        #A = getRandomMatrix(n)
        p = np.longdouble(G.o)
        #2. Sample a matrix A
        #3.Create hash key output; Pillar sign means Product from i=1 to n or over all elements i in set I
        hashkey = (Gg,p,generator), A
        return hashkey

    #G for generating algorithm takes as inputs a hash key hk and a predicate f element of Fn (predicate) (hk,fi) and outputs a pair of an encoding key ek and trapdoor td
    def generating_algorithm(self,sampling_algorithm): # done by the receiver; encoding_key be made public, trapdoor value must be kept private by the receiver
        #1.s;trapdoor: uniform integer t in Zp
        #g generates group Zp with g**k mod p with values between 1 and p-1 --s,t both element of Zp
        (G,p,g), A = sampling_algorithm
        s = np.longdouble(random.choice(G)) #s and t are trapdoor functions
        t = np.longdouble(random.choice(G))
        #2. Set
        u = g**s
        B = key_matrix(n,A,s,t,g)
        #key_1 = encoding_key[0][0] #TBD: replace by algorithm choosing random smaller matrix from key-matrix
        #key_2 = encoding_key[1][1]
        #3. Output
        ek = (u,B)
        td = (s,t)
        return ek,td
    #H for Hashing algorithm taking hash key hk, a string x element of {0,1}**n as well as randomness p_dense element of {0,1}* as input.
    #... and deterministically outputs a hash value h element of {0,1}**n_long

    def hashing_algorithm(self,sampling_algorithm,n): #done by the sender, receiver only gets hash-output
        (G,p,g), A = sampling_algorithm
        r = p
        H_x = hash_value_paper(A,r,g,n)
        #r = 5       #np.longdouble(random.choice(G))
        #full_hash = (g**r) * A_prod
        return H_x #like in yt

    #E(ek,x;p) -- Hinting -- The encoding algorithm takes as input an encoding key ek, string x element of {0,1}**n as well as randomness p_dense elemnt of {0,1}* as input.
    #..and deterministically outputs an encoding e element of {0,1}**w.
    def encoding_algorithm(self,generating_algorithm,sampling_algorithm,n): #encoding done by sender
        (G, p, g), A = sampling_algorithm
        (u,B) = generating_algorithm[0]
        H_x = hash_value_paper(B,p,u,n) # taken only x parts of key_nr => is that the whole encryption?
        #e = (u**r)*B_prod -> paper ansatz
        #ê = distance(e_key_nr)%2 #TBD
        #full_e = u_r * B_prod
        return H_x

    #D(td,h) -- Decoding -- The decoding algorithm takes as input a trapdoor td, a hash value h element of {0,1}**n_long
    #...and outputs a pair of a 0-encoding and a 1-necoding (e0,e1) element of {0,1}**w x {0,1}**w
    def decoding_algorithm(self,sampling_algorithm,hashing_algorithm,generating_algorithm,encoding_algorithm): #decoding is done by receiver but problem is only needs generator value others are private to sender --> TBD
        (G, p, g), A = sampling_algorithm #imported for the generator needed but it seams as its not the generator meant but the g from matrix key -- as well receiver can't have access to full Matrix A,otherwise would not need encoding
        h = hashing_algorithm
        e = encoding_algorithm
        (s,t) = generating_algorithm[1]
        #h_s = [element ** s for element in h]
        h_s = h**s
        g_t = g**t
        #h_s_g_t = [element * g_t for element in h_s]
        h_s_g_t = h_s*g_t
        x_i=0
        #e_0 = [None] * (len(h_s))
        #e_1 = [None] * (len(h_s))
        e_0 = 0
        e_1 = 0
        #for i in range(len(h_s)):
        if e == h_s:
            x_i = 0
        if e == h_s_g_t:
            x_i = 1
        e_0 = h_s
        e_1 = h_s_g_t
        return e_0,e_1 #geben i keys aus hier

#aufgeschrieben wegen fehlender Variation, kann aber gar nicht mehr haben, da maximal eine Kolonne/ein e0,e1 für x[i] gefunden werden kann; d.h. nur e0[i],e1[i] per key i ausgeben
        ##4.2.2.Augmentation to rate-1 TDH in the expense of a λ1 error probability

if __name__ == '__main__':
    lambda_var = 2                  #int(raw_input("Enter lambda value: "))
    n = 10                            #int(raw_input("Enter input length: "))
    sampling_algorithm = TDH(lambda_var,n).sampling_algorithm(lambda_var,n)
    generating_algorithm = TDH(lambda_var,n).generating_algorithm(sampling_algorithm)
    hashing_algorithm = TDH(lambda_var,n).hashing_algorithm(sampling_algorithm,n)
    encoding_algorithm = TDH(lambda_var,n).encoding_algorithm(generating_algorithm,sampling_algorithm,n)
    decoding_algorithm = TDH(lambda_var,n).decoding_algorithm(sampling_algorithm,hashing_algorithm,generating_algorithm,encoding_algorithm)
    print(generating_algorithm[0][1])
    print(decoding_algorithm)
