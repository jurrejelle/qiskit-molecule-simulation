import json
import pprint
from qiskit.algorithms.minimum_eigensolvers import NumPyMinimumEigensolver
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_nature.second_q.mappers import QubitConverter, ParityMapper
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver


# Setup dicts
avg_ansatzes = {}
avg_optimizers = {}
avg_mappings = {}

mae_ansatzes = {}
mae_optimizers = {}
mae_mappings = {}

qubits = {}

print_type = "pretty_print" # latex or pretty_print

# Calculate the actual eigenvalue to calculate the Mean Absolute Error
driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.740848",
    basis="sto3g",
    charge=0,
    spin=0,
    max_memory=30760,
    unit=DistanceUnit.ANGSTROM,
)
problem = driver.run()


converter = QubitConverter(ParityMapper())
numpy_solver = NumPyMinimumEigensolver()

calc = GroundStateEigensolver(converter, numpy_solver)
res = calc.solve(problem)
actual = res.raw_result.eigenvalue



filename = "output_h2.json"

with open(filename, "r") as f:
    output = json.loads(f.read())

print(len(output))

# Aggregate data
for item in output:
    ident = [item["mapper"], item["ansatz"], item["optimizer"]]
    if item["ansatz"] not in avg_ansatzes:
        avg_ansatzes[item["ansatz"]] = 0
    if item["optimizer"] not in avg_optimizers:
        avg_optimizers[item["optimizer"]] = 0
    if item["mapper"] not in avg_mappings:
        avg_mappings[item["mapper"]] = 0
    avg_mappings[item["mapper"]] += item["time"]
    avg_optimizers[item["optimizer"]] += item["time"]
    avg_ansatzes[item["ansatz"]] += item["time"]


    mae = abs(item['eigenvalue'] - actual)
    if item["ansatz"] not in mae_ansatzes:
        mae_ansatzes[item["ansatz"]] = 0
    if item["optimizer"] not in mae_optimizers:
        mae_optimizers[item["optimizer"]] = 0
    if item["mapper"] not in mae_mappings:
        mae_mappings[item["mapper"]] = 0

    mae_mappings[item["mapper"]] += mae
    mae_optimizers[item["optimizer"]] += mae
    mae_ansatzes[item["ansatz"]] += mae

    if item["qubits"] not in qubits.keys():
        qubits[item["qubits"]] = []

    qubits[item["qubits"]].append(ident)

# Normalize
for ansatz in avg_ansatzes:
    avg_ansatzes[ansatz] /= sum([1 for item in output if item['ansatz'] == ansatz])
    mae_ansatzes[ansatz] /= sum([1 for item in output if item['ansatz'] == ansatz])

for mapping in avg_mappings:
    avg_mappings[mapping] /= sum([1 for item in output if item['mapper'] == mapping])
    mae_mappings[mapping] /= sum([1 for item in output if item['mapper'] == mapping])

for optimizer in avg_optimizers:
    avg_optimizers[optimizer] /= sum([1 for item in output if item['optimizer'] == optimizer])
    mae_optimizers[optimizer] /= sum([1 for item in output if item['optimizer'] == optimizer])

def print_dict(mydict):
    if print_type == "latex":
        for key, value in sorted(mydict.items(), key=lambda x: x[1]):
            print(f"{key} & {value:10f} \\\\".replace("_","\\_"))
    elif print_type == "pretty_print":
        pprint.pprint(mydict)
    print("="*40)

print(f"{'='*20}Average times per system{'='*20}")
print_dict(avg_ansatzes)
print_dict(avg_optimizers)
print_dict(avg_mappings)

print(f"{'='*20}Mean Absolute Error per system{'='*20}")
print_dict(mae_ansatzes)
print_dict(mae_optimizers)
print_dict(mae_mappings)


for item in qubits:
    print(f"{item}: {len(qubits[item])}")