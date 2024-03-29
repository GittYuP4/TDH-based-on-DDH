import numpy as np
import random
from TDH_functions import *
import matplotlib.pyplot

from groups import Group #https://github.com/Smeths/pygroup

#Goal: Implement the Trapdoor hash function from DDH assumption


#4.2. TDH for Index Predicates from DDH
##4.2.1“basic” construction of a rate-1/λ TDH scheme for index predicates
#S for Sampling Algorithm with inputs security parameter lambda and input length n (1^lambda,1^n)
#..and outputing as hash key hk

#1 1. Sample (G; p; g); Multiplicative abelian group G of prime order p, with a public generator g
G = Group("mult",19)
p = G.o
g = np.array(G.gcycle(p)) #g**lambda mod p
for i in g:
    if i != 1:
        g = i
#2. Sample a matrix A
n = 10
A = getBinaryMatrix(n)
#3.Create hash key output; Pillar sign means Product from i=1 to n or over all elements i in set I
h = hash_value(A,n)
print(h)

#G for generating algorithm takes as inputs a hash key hk and a predicate f element of Fn (predicate) (hk,fi) and outputs a pair of an encoding key ek and trapdoor td
#1.s;trapdoor: uniform integer t in Zp
#g generates group Zp with g**k mod p with values between 1 and p-1 --s,t both element of Zp
s = random.choice(G.g())
t = random.choice(G.g())
#2. Set
u = np.power(g,s)
key = key_matrix(n,A,s,t,g)
print(key)
#3. Output
ek = (u,key)
td = (s,t)

#H for Hashing algorithm taking hash key hk, a string x element of {0,1}**n as well as randomness p elemnt of {0,1}* as input.
#... and deterministically outputs a hash value h element of {0,1}**n
r = random.choice(G.g())
h = (g**r) * A
print(h)
#E(ek,x;p) -- Hinting -- The encoding algorithm takes as input an encoding key ek, string x element of {0,1}**n as well as randomness p elemnt of {0,1}* as input.
#..and deterministically outputs an encoding e element of {0,1}**w.
e = u**r * hashkey(key,n)
print(e)

#D(td,h) -- Decoding -- The decoding algorithm takes as input a trapdoor td, a hash value h element of {0,1}**n_long
#...and outputs a pair of a 0-encoding and a 1-necoding (e0,e1) element of {0,1}**w x {0,1}**w
e0 = h**s
e1 = h**s * g**t
print(e0)
print(e1)

##4.2.2.Augmentation to rate-1 TDH in the expense of a λ1 error probability


