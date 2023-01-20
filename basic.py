from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.providers.basicaer import QasmSimulatorPy

# Create bell states
# --- H -- o ---
#          |  
# ---------x ---
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0,1], [0,1])

backend_sim = QasmSimulatorPy()
transpiled_qc = transpile(qc, backend_sim)

result = backend_sim.run(transpiled_qc).result()
print(result.get_counts(qc))
