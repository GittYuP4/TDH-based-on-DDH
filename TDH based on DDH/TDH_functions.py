from random import randint
import numpy as np
#https://stackoverflow.com/questions/27784465/how-to-randomly-get-0-or-1-every-time
def getMatrix (n):

    matrix = (
        [str(randint(0, 1)) for _ in range(0, n)] for _ in range(0, 2)
    )
    #for row in matrix:
     #   print("".join(row))

    return matrix

def hashkey(A,n):
    n = n
    hk = 1
    for row in A:
        for column in A:
            hk = A[row][column]*hk
    return hk
