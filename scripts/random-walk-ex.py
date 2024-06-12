from random import choice
import matplotlib.pyplot as plt
import numpy as np


def main():
    
    def secexp(T = 6):
        N = T**2 
        D = 4
        AG = np.zeros((N,N))
        for i in range(N-1): 
            for k in np.random.choice([ (i+1)%T+ T*j for j in range(0,T-1)], size=(D), replace=False):
                AG[i][k] = 1
                AG[k][i] = 1
        for i in range(N):
            if sum(AG[i]) > 0:
                AG /= sum(AG[i])
                AG[i][i] = -1

        #print(AG)
        AG =  - AG 
        np.set_printoptions(precision=3)
        if np.isnan(AG).any():
            return 0
        L = list(np.linalg.eigvals(AG))
        L = sorted(list(map(abs, L)))
        print(L)
        #maxeig = max(L)
        #L.remove(maxeig)
        #ret = (maxeig - max(L)) #/maxeig
        ret =  sorted(L)[1]
        print(ret)
        return ret

    def main1(T = 3):
        def singleexp(T = 3):
            t, l = 0, 0
            V = [ ]
            while t < T:
                V.append(t)
                if t == 0:
                    t += 1
                else:
                    t += choice([-1,1]) 
            AG = np.zeros((len(V),len(V)))
            for i, iv in enumerate(V):
                for j, jv in enumerate(V):
                    if abs(iv - jv) == 1:
                        if choice([True, True]):
                            AG[i][j] = 1 
                            AG[j][i] = 1
            for i in range(len(V)):
                AG[i] /= sum(AG[i]) if sum(AG[i]) > 0 else 1
            AG = np.eye(len(V)) - AG 
            np.set_printoptions(precision=3)
            if np.isnan(AG).any():
                return 0
            L = list(np.linalg.eigvals(AG))
            L = sorted(list(map(abs, L)))
            print(L)
            #maxeig = max(L)
            #L.remove(maxeig)
            #ret = (maxeig - max(L)) #/maxeig
            ret =  sorted(L)[1] 
            print(AG)
            print(ret)
            return ret
        return singleexp(T)

    _range = range(7,40)
    f = [    max( [ secexp(T) for _ in range(30)]) for T in _range ]
    plt.plot( f) 
    plt.show()
if __name__ == "__main__":
    main() 
