from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit_symbolic import Operator

# Use Aer's AerSimulator
simulator = AerSimulator()

# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(5, 2)


# Add a H gate on qubit 0
circuit.h(1)
circuit.cx(1,2)
circuit.h(3)
circuit.cx(3,4)
circuit.h(0)

circuit.cswap(0,1,3)
circuit.cswap(0,2,4)
#circuit.cswap(7,3,6)

#circuit.cx(1, 10)
#circuit.cx(2, 11)
#circuit.cx(3, 12)
#circuit.cx(4, 13)
#circuit.cx(5, 14)
#circuit.cx(6, 15)
#circuit.h(7)
#circuit.cswap(7,10,13)
#circuit.cswap(7,11,14)
#circuit.cswap(7,12,15)
#
###circuit.cx(3, )
circuit.h(0)
#circuit.h(9)
# Add a CX (CNOT) gate on control qubit 0 and target qubit 1
#circuit.cx(0, 1)

# Map the quantum measurement to the classical bits
#circuit.measure([7 ], [0])
op = Operator.from_circuit(circuit)
#circuit.measure([19], [2])
# Compile the circuit for the support instruction set (basis_gates)
# and topology (coupling_map) of the backend
compiled_circuit = transpile(circuit, simulator)

# Execute the circuit on the aer simulator
#job = simulator.run(compiled_circuit, shots=1000, memory=True)
# Grab results from the job
#result = job.result()

#print(result.get_memory())
print(circuit.draw())
# Returns counts
#counts = result.get_counts(compiled_circuit)
#print("\nTotal count for 0 and 1 are:", counts)

from sympy import init_printing
init_printing() 
print(op.to_sympy())
# Draw the circuit

