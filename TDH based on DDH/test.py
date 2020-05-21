import numpy as np
import random
import matplotlib.pyplot
from pip._vendor.distlib.compat import raw_input
from TDH_functions import *

from groups import Group #https://github.com/Smeths/pygroup

G = Group("mult", 199)
Gg = G.g()
p = G.o
g = np.array(G.gcycle(p))
rand_elem_1 = np.array(np.random.choice(p, 10)).astype(int)
rand_elem_2 = np.array(np.random.choice(p, 10)).astype(int)

arr = np.concatenate(([rand_elem_1],[rand_elem_2]))
print(arr)
#random_matrix = np.array([np.random.choice((G), 10)]