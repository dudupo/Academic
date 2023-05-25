from matplotlib import pyplot as plt 
import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True

def compare():
   
    ef = lambda x : -x*np.log2(x) - (1-x)*np.log2(1-x)
    for k in range(1,10):
        g = lambda x,y : ( 1 - 2* ef(x))**2 + (k+1)/(2*k)*(x/4)
        h = lambda x : g(x,k)
        s = np.linspace(0,1,200)
        t = s[ef(s) <= 0.5]
        plt.plot(t, np.ones(len(t))* (2*k+1)/(2*k))
        plt.plot(t, h(t))
        plt.show()


def main():

    functions = [ lambda x : 1 - x, lambda x : (8/5)* ( (9/8)  - x) ]
    t = np.linspace(0,1,600)
     
    for f, color in zip(functions, ["black", "gray"]):
        plt.plot(t[ np.logical_and( 0 <= f(t) , f(t) <= 1 ) ],f(t)[ np.logical_and( 0 <= f(t) , f(t) <= 1)  ], c=color)

    plt.title(r"$ \rho,\delta$ trade-of ")
    plt.legend([r"Singlethon", "us" ])
    plt.xlabel(r"$ \rho $ ")
    plt.ylabel(r"$ \delta $ ")
    import tikzplotlib
    tikzplotlib.save("../projects/NLTES_project/singleton.tex")
    plt.clf()


if __name__ == "__main__":
    compare()
