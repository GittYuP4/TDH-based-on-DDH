import numpy as np
import random
import matplotlib.pyplot
from pip._vendor.distlib.compat import raw_input
from TDH_functions import *
import hashlib

from groups import Group #https://github.com/Smeths/pygroup
G = Group("mult", 15)
Gg = G.g()
p = G.o
g = np.array(G.gcycle(p))
rand_elem_1 = np.array(np.random.choice(p, 10)).astype(int)
rand_elem_2 = np.array(np.random.choice(p, 10)).astype(int)
A = np.concatenate(([rand_elem_1], [rand_elem_2])).astype('int64')


#https://www.thesslstore.com/blog/difference-sha-1-sha-2-sha-256-hash-algorithms/ -- Sha1,2 erklärt
#https://www.geeksforgeeks.org/sha-in-python/ -- SHA, ( Secure Hash Algorithms )
#RSA's MD5: 128 bit hash value similiar to SHA1: The 160 bit hash function that resembles MD5 hash in working and was discontinued to be used seeing its security vulnerabilities.
result = hashlib.md5(A.encode())
print(result.hexdigest())

#The variety of SHA-2 hashes can lead to a bit of confusion, as websites and authors express them differently.
#If you see “SHA-2,” “SHA-256” or “SHA-256 bit,” those names are referring to the same thing. If you see “SHA-224,” “SHA-384,” or “SHA-512,” those are referring to the alternate bit-lengths of SHA-2.
A = str(A)
result = hashlib.sha256(A.encode()) #This hash function belong to hash class SHA-2, the internal block size of it is 32 bits.
print(result.hexdigest())


