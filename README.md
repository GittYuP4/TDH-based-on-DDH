# Cryptography and Security Protocols project
## An implementation of chapter 4.2. from Trapdoor Hash Functions and Their Applications by Döttling et al. 2019.

I was the first person implementing this paper. I did it on my own during my univsersity course 'Cryptography and Security Protocols' in my exhange semester at IST Lisbon. I got 19 out of 20 points in the final evaluation.

The whole code is implemented in the class TDH() in the TDH_implementation.py file. It contains a constructor and 5 more methods. In the TDH functions.py file, additional help functions have been created. The constructor simply initializes n, lambda and rate_1 which can be chosen by the user.

Compared with the pure trapdoor function, where the receiver can reactivate the entire input x with the help of a trapdoor, TDH's only restore a part of x (x[i]). The sender privacy is guaranteed by hashing, the x obscured by h. The receiver privacy by index i, contained in the key creation.

The code implementation is strongly based on the paper mentioned in the title. Other sources have been remarked in the code itself. For the sampling_algorithm the pygroup repository (smeths) has been used to calculate abelian groups, its generators and orders. Moreover, the prng repository (firaja) has been used to build a pseudorandom number generator and been combined with the values from the distance function from chapter 4.2.2 to make a rate 1 possible. Depending on if one sets rate_1 to true or not, the code is executed without or with rate 1.

