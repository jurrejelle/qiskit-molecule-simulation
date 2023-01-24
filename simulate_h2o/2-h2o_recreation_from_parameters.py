
import json
import time

from qiskit.algorithms.minimum_eigensolvers import VQE, NumPyMinimumEigensolver, VQEResult
from qiskit.algorithms.optimizers import SLSQP
from qiskit.circuit import Parameter
from qiskit.circuit.library import TwoLocal
from qiskit.circuit.parametervector import ParameterVectorElement
from qiskit.primitives import Estimator
from qiskit_nature.second_q.algorithms import VQEUCCFactory, GroundStateEigensolver
from qiskit_nature.second_q.circuit.library import *
from qiskit_nature.second_q.mappers import QubitConverter, JordanWignerMapper, BravyiKitaevMapper, ParityMapper
from qiskit_nature.second_q.problems import ElectronicStructureProblem
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver

# Params for h2 if you haven't simulated h2o yet
# Swap out the atom to h2 as well if you want to use these

#params = [2.4880008478017135e-08,  -3.495203492544701e-08, -0.11294958541888067]

with open("output.txt", "r") as f:
    output = json.loads(f.read())

params = [output["optimal_parameters"][f"t[{x}]"] for x in range(0, len(output["optimal_parameters"]))]

H2  = "H 0 0 0; H 0 0 0.740848"
H2O = "H 0.75754079778 0.58707963658 0; O 0 0 0; H -0.75754079778 0.58707963658 0"

driver = PySCFDriver(
    atom=H2O,
    basis="sto3g",
    charge=0,
    spin=0,
    max_memory=30760,
    unit=DistanceUnit.ANGSTROM,
)
problem: ElectronicStructureProblem = driver.run()

converter = QubitConverter(ParityMapper())

ucc = UCCSD()

ucc.qubit_converter = converter
ucc.num_particles = problem.num_alpha, problem.num_beta
ucc.num_spatial_orbitals = problem.num_spatial_orbitals

bound_params = dict(zip(ucc.parameters, params))
ucc.assign_parameters(bound_params, inplace=True)
with open("output_qasm.txt", "w") as f:
    f.write(ucc.decompose(reps=100).qasm())