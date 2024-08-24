from sage.all import *
from itertools import product

def extract_trig(Cgens, Triggens):
    triples =  matrix( GF(2), [ [ sum((u.pairwise_product(v)).pairwise_product(w)) for v,w in product(Cgens, Cgens) ]\
                                for u in Triggens ])
    trigbase = kernel(triples)
    return trigbase

if __name__ == "__main__":
    for _ in range(2000):
        C = codes.random_linear_code(GF(2), 20, 13)
        Cp = C.dual_code()
        SynMat = Cp.generator_matrix() * Cp.generator_matrix().transpose()
        X = kernel(SynMat)
        if X.dimension() > 0:
            Triggens = extract_trig(C.gens(), [ Cp.generator_matrix().transpose() *x for x in X.gens() ])
            if Triggens.dimension() > 0:
                print(Triggens.dimension())
             
    
