
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

params = [2.4880008478017135e-08,  -3.495203492544701e-08, -0.11294958541888067]
# Once h2osolver.py runs, import params into here and change it to h2o

H2  = "H 0 0 0; H 0 0 0.740848"
H2O = "H 0.75754079778 0.58707963658 0; O 0 0 0; H -0.75754079778 0.58707963658 0"

driver = PySCFDriver(
    atom=H2,
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
print(ucc.qasm())