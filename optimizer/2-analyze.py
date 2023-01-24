import json
import pprint
filename = "output_h3.json"

avg_ansatzes = {}
avg_optimizers = {}
avg_mappings = {}

mae_ansatzes = {}
mae_optimizers = {}
mae_mappings = {}

qubits = {}
with open(filename, "r") as f:
    output = json.loads(f.read())

actual = sum([item['eigenvalue'] for item in output])/len(output)
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

print("f{'='*20}Average times per system{'='*20}")
pprint.pprint(avg_ansatzes)
pprint.pprint(avg_optimizers)
pprint.pprint(avg_mappings)

print("f{'='*20}Mean Absolute Error per system{'='*20}")
pprint.pprint(mae_ansatzes)
pprint.pprint(mae_optimizers)
pprint.pprint(mae_mappings)


for item in qubits:
    print(f"{item}: {len(qubits[item])}")