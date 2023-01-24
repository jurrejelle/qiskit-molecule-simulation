from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeCairo

# To get data from a real quantum computer, get the backend from e.g. ibmq
# However, since we don't have access to a real quantum computer with >14 qubits, we're using IBM Cairo
# See: https://quantum-computing.ibm.com/services/resources?tab=systems&system=ibm_cairo
backend = FakeCairo()

gate_times = {}
gate_errors = {}
unit = ""

# Retrieving gate times and error rates for all gates available on this quantum computer
for gate in backend.properties().gates:
    for parameter in gate.parameters:
        if(parameter.name == 'gate_error'):
            gate_errors[gate.gate] = parameter.value
        if(parameter.name == 'gate_length'):
            gate_times[gate.gate] = parameter.value
            unit = parameter.unit

print(gate_times)

# Transpile the circuit to be as it would run on Cairo
qc = QuantumCircuit.from_qasm_file("output_qasm.txt")
print(f"Before transpilation: {qc.count_ops()}")

t_qc = transpile(qc,
                 backend,
                 optimization_level=0,
                 seed_transpiler=0)

print(f"After transpilation: {t_qc.count_ops()}")
# Add up the sum of all times, and multiply errors
total_time = 0
total_accuracy = 1
for operation, amount in t_qc.count_ops().items():
    total_time += gate_times[operation] * amount
    total_accuracy *= (1-gate_errors[operation]) ** amount
print(f"Total time: {total_time:2f}{unit}")
print(f"Total accuracy: {total_accuracy}")