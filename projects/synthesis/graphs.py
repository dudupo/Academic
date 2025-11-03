

import numpy as np
from math import log
from matplotlib import pyplot as plt 


def q_power(q, mu = 0.1, delta2 = 4 ):
    power =  ( (delta2 - 1) * log(2,q) +1)* (0.5- mu) + log(2,q) 
    return power

if __name__ == "__main__":
    X = [0.001, 0.005, 0.01, 0.05, 0.075 ]
    plt.plot( X, [ q_power(q) for q  in X ] )   
    plt.xlabel('q') 
    plt.ylabel('exponent')
    plt.savefig('exponent_q.svg') 





