from sympy import * 

from sympy import sqrt
from sympy.physics.quantum.qubit import Qubit, measure_partial_oneshot
from sympy.physics.quantum.gate import HadamardGate as H, Z, CGate
from sympy.physics.quantum.qapply import qapply

def exp():
    #q1, q2 = Qubit('0'), Qubit('1')
    psi = 1/2*( sqrt(3)* Qubit('00')+ Qubit('01'))
    print(psi)
    Cz = CGate( (0) , Z(1)) 
    for _ in range(10):
        psi = qapply( H(0)*  Cz * H(0) * psi)
        print(psi)
        psi = measure_partial_oneshot(psi, (0,))
        print(psi)
    # Hadamard on bell state, applied on 2 qubits.
    #psi = 1/sqrt(2)*(Qubit('00')+Qubit('11'))
    #qapply(HadamardGate(0)*HadamardGate(1)*psi)

# 116 $ \left( 1 -d_{T}/2  \right)^{2}\Delta^{2} \le d_{T}\delta_{0}\Delta <++>$

if __name__ == "__main__":
    exp()
    exit(0)
    d, D, l = symbols('d_{T} \Delta \delta_{0}')
    r1 = solveset(Eq( (( D - d/2) **2), d *l *D  ), d)
    # print(latex(series(list(r1)[0], l, n=3)))
    r2 = solveset(Eq( (( D - d/2) **2)  + 2 * (D**(3/2)) , d*l*D/2  ), d)
    print(latex(series(list(r2)[1] , l, n = 3) ))
    #print(latex(r1))
    #print(latex(list(r2)[0].subs({l:2/3})))
