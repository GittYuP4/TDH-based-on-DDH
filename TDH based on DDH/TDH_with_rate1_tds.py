import sys
from TDH_functions import *
from scipy.linalg import norm

#*************************************************************
# Title: pygroup - Abelian Group class
# Author: John Smethurst - Smeths
# Date: 2017
# Code version: 1.0
# Availability: https://github.com/Smeths/pygroup
#*************************************************************
from groups import Group

class TDH(object):

    def __init__(self,lambda_var,n,rate_1):
        self.lambda_var = lambda_var #the higher lambda the less predictable the bits
        self.n = n
        self.rate_1 = rate_1
    #Sampling_algorithm to find hashkey with abelian groups
    def sampling_algorithm(self): # done by the sender, output also private and only used in the hashing_algorithm again by the sender
        # 1. Sample (G; p; g); (Finite-) multiplicative abelian group G of prime order p, with a public generator g
        G = Group("mult", 7)
        Gg = G.g() #Group list representation
        p = np.longdouble(G.o) #order of G
        generators_of_G = []
        for i in Gg: #finding generator of Group G
            x = np.array(G.gcycle(i))
            x_sorted = np.sort(x)
            if np.array_equal(Gg,x_sorted):
                generators_of_G.append(i)
        generator = np.longdouble(random.choice(generators_of_G))
        # 2. Sample a matrix A
        rand_elem_1 = np.array(np.random.choice(Gg, 10), dtype=np.longdouble)
        rand_elem_2 = np.array(np.random.choice(Gg, 10), dtype=np.longdouble)
        A = np.concatenate(([rand_elem_1], [rand_elem_2]))
        #3.Create hash key output; Pillar sign means Product from i=1 to n or over all elements i in set I
        r = np.longdouble(random.randint(0, p - 1))
        hashkey = (Gg,p,generator),A,r
        return hashkey

    #Generating_algorithm to create a pair of an encoding key ek and a trapdoor td
    def generating_algorithm(self,sampling_algorithm,lambda_var,n): # done by the receiver; encoding_key be made public, trapdoor value must be kept private by the receiver
        #1. create trapdoors s and t
        (G,p,g),A,r = sampling_algorithm
        s = np.longdouble(random.randint(0,p-1))
        t = np.longdouble(random.randint(0,p-1))
        K = lambda_var
        #2. Set
        u = g**s
        B = key_matrix(n,A,s,t,g)
        #3. Output
        ek = (u,B,t,K)
        td = (s,t,K)
        return ek,td

    #Hashing_algorithmto find a hash value h element of length n
    def hashing_algorithm(self,sampling_algorithm,n): #done by the sender, receiver only gets hash-output
        (G,p,g),A,r = sampling_algorithm
        H_x = hash_value_paper(A,g,r,n)
        return H_x

    #Creating a hint e depending if rate_1 is chosen or not
    def encoding_algorithm(self,generating_algorithm,sampling_algorithm,n,rate_1): #encoding done by sender
        (G,p,g),A,r = sampling_algorithm
        (u,B,t,K) = generating_algorithm[0]
        e = hash_value_paper(B,u,r,n)
        delta = (1 / K)
        if rate_1 == 'yes':
            g_t = int(g ** t)
            e = function_G(e,K,g_t,p,1,delta)
        return e

    #Decoding_algorithm restoring the element of x[i] and returning e_0 and e_1
    def decoding_algorithm(self,sampling_algorithm,hashing_algorithm,generating_algorithm,encoding_algorithm,rate_1): #decoding is done by receiver but problem is only needs generator value others are private to sender --> TBD
        (G, p, g),A,r = sampling_algorithm #imported for the generator needed but it seams as its not the generator meant but the g from matrix key -- as well receiver can't have access to full Matrix A,otherwise would not need encoding
        h = hashing_algorithm
        e = encoding_algorithm
        (s,t,K) = generating_algorithm[1]
        h_s = h**s
        g_t = g**t
        h_s_g_t = h_s*g_t
        if rate_1 == 'yes':
            g_t = int(g_t)
            delta = 1 / K
            e_0 = h_s
            e_1 = h_s*g
            e_0 = function_G(e_0,K,g_t,p,1,delta)
            e_1 = function_G(e_1,K,g_t,p,1,delta)
            return e_0, e_1
        if rate_1 == 'no':
            print("Rate is",(1 / norm(e)))
            e_0 = h_s
            e_1 = h_s_g_t
            if e == h_s:
                x_i = 0
                print("x**i is", x_i)
                return e_0, e_1
            if e == h_s_g_t:
                x_i = 1
                print("x**i is", x_i)
                return e_0, e_1

def main():
    yes = {'yes', 'y', 'ye'}
    no = {'no', 'n',''}

    rate_1 = 'n'   #raw_input("Do you want the code to run with rate 1?").lower()
    if rate_1 in yes:
        rate_1 = 'yes'
    elif rate_1 in no:
        rate_1 = 'no'
    else:
        sys.stdout.write("Please enter with either 'yes' or 'no' again")

    lambda_var = 4   #int(raw_input("Enter lambda value: "))
    n = 10   #int(raw_input("Enter input length: "))
    sampling_algorithm = TDH(lambda_var,n,rate_1).sampling_algorithm()
    generating_algorithm = TDH(lambda_var,n,rate_1).generating_algorithm(sampling_algorithm,lambda_var,n)
    hashing_algorithm = TDH(lambda_var,n,rate_1).hashing_algorithm(sampling_algorithm, n)
    encoding_algorithm = TDH(lambda_var,n,rate_1).encoding_algorithm(generating_algorithm, sampling_algorithm,n,rate_1)
    decoding_algorithm = TDH(lambda_var,n,rate_1).decoding_algorithm(sampling_algorithm, hashing_algorithm, generating_algorithm, encoding_algorithm,rate_1)
    print(encoding_algorithm)
    print(decoding_algorithm)

if __name__ == '__main__':
    main()
