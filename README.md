# My Research

### Local Testability and qPCP
I have been dedicating most of my time to researching quantum local testable codes. I am trying to gain a deep understanding of the recent constructions and have attempted to remove the robustness assumption. Unfortunately, I didn't succeed to do so, and believe that this assumption is necessary, which limits the local structure to a narrow range. The first link shows my failed attempt to remove the w-robustness, and the second link shows that the polynomial code cannot form a $w$-robustness code.

1. [Remove the w-robustness (fail attempt)](https://github.com/dudupo/Academic/blob/master/projects/pdfs/ldpc_ltc.pdf).    
2. [The polynomial code is not w robust](https://github.com/dudupo/Academic/blob/master/projects/pdfs/poly_qldpc.pdf).

### No-Existence Of Generalized Diffusion.
We have used a known lower bound on the number of rounds required to compute the disjointness in a two-party (quantum) computation setting to show the impossibility of projecting over a given general state (literally given, without the classical description). This result, though seemingly trivial, was difficult to prove using standard methods (e.g., demonstrating non-linearity as in the no cloning theorem). However, the contradiction of previous communication results is obtained almost immediately [arxiv](https://arxiv.org/pdf/2304.03960.pdf), demonstrating the impossibility of generalized diffusion.

### Reducing the Depth of Hamiltonian Simulation Circuits
We are attempting to develop an efficient simulation circuit for a given Hamiltonian in the computational basis. Our goal is to create a technique that can be used for practical computations in the future. We assume properties such as the distribution of local terms along the circuit that match the expected behavior of nature. The [draft](https://github.com/dudupo/Academic/blob/master/projects/pdfs/Classiq.pdf) is still a work in progress and may contain mistakes, faults, and changes in notation :see_no_evil:.


### Quantum Version of FLP Impossibility: Achieving Reliability in a Quantum Distributed Environment
We are attempting to formulate a quantum version of the Stren proof, which states that it is impossible to perform asynchronous computation without a non-vanishing probability of non-termination. By doing so, we hope to achieve reliability in a quantum distributed environment.

### Groverizing Recent Results in the Era of Parameterized Complexity
We are not introducing any new concepts or proofs here, but rather assembling existing pieces together. [Draft](https://github.com/dudupo/Academic/blob/master/projects/pdfs/montone_local_search.pdf).

## Are you interested in collaborating in any way?
If so, feel free to request a pull, open an issue, or send an email.
