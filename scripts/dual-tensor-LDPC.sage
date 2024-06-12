import sage.coding.linear_code as lnc
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
import datetime
import pickle as pkl
class DualTensorCode(lnc.LinearCode):


    def __init__(self, codeA, codeB):
        self.codeA, self.codeB = codeA, codeB
        gen = lnc.LinearCode(codeA.dual_code().product_code(\
                codeB.dual_code())).dual_code().generator_matrix()
        super().__init__(gen)

    def reshape_to_matrix(self, element):
        return element.numpy().reshape((self.codeA.length( ), self.codeB.length( )))
    def random_test_case(self):
        return self.reshape_to_matrix(self.random_element())    
    def codes(self):
        return [ self.codeA, self.codeB ] 

    def decompose(self, element):
        decoders = [ codes.decoders.LinearCodeNearestNeighborDecoder(C) for C in self.codes() ] 
        codeword = self.reshape_to_matrix(element)
        parts = [ [], [] ]
        for i, decoder in enumerate(decoders):
            for raw in codeword:
                parts[i].append(decoder.decode_to_code(\
                        vector( GF(2), raw.tolist() )))
            codeword = codeword.transpose()
        return parts

    def count_support(self, element):
        def nonzeor(v):
            for u in v:
                if u != 0:
                    return 1
            return 0
        parts = self.decompose(element)
        return [sum(map(nonzeor, part)) for part in parts]



def sample_light_codewords(code, T, _filter):
    while T > 0: 
        codeword = code.random_element()
        print(codeword.hamming_weight())
        lifes = 200
        while (codeword.hamming_weight() > _filter):
       #     print(codeword.hamming_weight())
            codeword = code.random_element()
            lifes -= 1
            if lifes <= 0:
                yield False, False
        yield True, codeword
        T -= 1

def w_robust_check(code):
    print(code.length())
    T, X, Y = 100, [], []
    for flag, codeword in sample_light_codewords(code,T,code.length()^(3/4)):
        if not flag:
            return False 
        Y.append(sum(code.count_support(codeword)))
        X.append(codeword.hamming_weight())
    plt.scatter(X,Y, c="black", s=5)
    plt.savefig(f"./svg/exp-{code.length()}-{code.dimension()}-{datetime.datetime.now()}.svg")
    pkl.dump(code, open(f"./pkl/exp-{code.length()}-{code.dimension()}-{datetime.datetime.now()}.pkl", "bw"))
    #weight = np.sum(codeword)
    return True    
def test_Dual_Tensor_basics():
    flag = False
    while not flag:
        C = codes.random_linear_code(GF(2), 40, 15) 
        G = DualTensorCode(C,C)    
        flag = w_robust_check(G)

test_Dual_Tensor_basics()



