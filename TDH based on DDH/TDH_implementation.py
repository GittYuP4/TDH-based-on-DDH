import numpy as np
import random
from TDH_functions import *

#Goal: Implement the Trapdoor hash function from DDH assumption

#4.2. TDH for Index Predicates from DDH

##4.2.1“basic” construction of a rate-1/λ TDH scheme for index predicates
#S(1^lambda,1^n):
#2. Sample a matrix A
n = 10
A = getMatrix(n)
#3.Create hash key output; Pillar sign means Product from i=1 to n or over all elements i in set I
for row in A:
     print("".join(row))

hk = hashkey(A,n)
print(hk)



##4.2.2.Augmentation to rate-1 TDH in the expense of a λ1 error probability


#6 Applications of Rate-1 OT from 4.2.2.


#7 Private Laconic OT


