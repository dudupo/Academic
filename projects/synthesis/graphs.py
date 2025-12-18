

import numpy as np
from math import log
from matplotlib import pyplot as plt 
import sys
sys.setrecursionlimit(10000)

def q_power(q, mu = 0.1, delta2 = 4 ):
    power =  ( (delta2 - 1) * log(2,q) +1)* (0.5- mu) + log(2,q) 
    return power

def plot_q_power():
    X = [0.001, 0.005, 0.01, 0.05, 0.075 ]
    plt.plot( X, [ q_power(q) for q  in X ] )   
    plt.xlabel('q') 
    plt.ylabel('exponent')
    plt.savefig('exponent_q.svg') 

def qp_diff(q, p, n, t):
    if t == 0:
        return [ ]
    else:
        b = 1 - (1/np.sqrt(n))
        z = q**b #+ p 
        return [z] + qp_diff(z,p,n,t-1)





def check_fail(delta = 8):

    Y1, Y2 = [ ], [ ]
    for p in np.linspace(0.0001, 0.001, num = 1000):
        Y2.append( ( 0.5* ( 1 - ( 1 - 2*p)**delta ) )**2 ) 
        Y1.append(  p ) 


    plt.plot(Y1)
    plt.plot(Y2)
    plt.show()













if __name__ == "__main__":



    check_fail()

    exit(0)

    #Y = list(range(100,10000,50))
    X, Z = [], []
    for n in [100, 200, 400, 500, 700, 800, 900, 1000, 1200, 1300, 1400, 1500]: 
        a = 1 - (1/np.sqrt(n))
        #X = range(200)
        Y = qp_diff(0.01,0.01, n, 200)
        #plt.plot( X, Y)   
        X.append(n)
        Z.append(Y[int(np.pow(n, 1/2))])
    plt.plot(X,Z)
    plt.xlabel('n') 
    plt.ylabel('diff')
    plt.savefig('diff_exponent_q.svg') 





