import numpy as np
import random
from TDH_functions import *
import matplotlib.pyplot

#Goal: Implement the Trapdoor hash function from DDH assumption

#4.2. TDH for Index Predicates from DDH

##4.2.1“basic” construction of a rate-1/λ TDH scheme for index predicates
#S(1^lambda,1^n):

#1 1. Sample (G; p; g); Multiplicative abelian group G of prime order p, with a public generator g
q = 3 #can we take any prime?
g = getGenerator(q)
#2. Sample a matrix A
n = 10
A = getBinaryMatrix(n)
print(A)
#3.Create hash key output; Pillar sign means Product from i=1 to n or over all elements i in set I
hk = hashkey(A,n)
print(hk)

#G(hk,fi)
#1.s;trapdoor: uniform integer t in Zp
s = random.randint(-1000,1000)
t = random.randint(-1000,1000)
#2.
u = g**s
print(key_matrix(n,A,s,t))


##4.2.2.Augmentation to rate-1 TDH in the expense of a λ1 error probability


#6 Applications of Rate-1 OT from 4.2.2.


#7 Private Laconic OT


