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


H2  = "H 0 0 0; H 0 0 0.740848"
He2 = "He 0. 0. 0.; He 3.1 0. 0"
HLi  = "H 0 0 0; Li 0 0 2"
CO2 = "O 0 0 0; C 0 0 1.158898; O 0 0 2.317796",
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
data = ""


def callback_fun(count, parameters, mean, metadata):
    global data
    curr = f"Iteration: {count}\nParameters: {parameters}\nMean: {mean}\n\n"
    data += curr


vqe_solver = VQEUCCFactory(Estimator(), UCCSD(), SLSQP())
converter = QubitConverter(ParityMapper())

calc = GroundStateEigensolver(converter, vqe_solver)

time_before_solve = time.time()
res = calc.solve(problem)
solve_time = time.time() - time_before_solve

raw_result: VQEResult = res.raw_result


with open("output.txt", "w") as f:
    optimal_params = {str(k.name):v for k,v in raw_result.optimal_parameters.items()}
    outputobj = {
        "optimal_parameters": optimal_params,
#        "raw_result": raw_result,
        "eigenvalue": raw_result.eigenvalue,
        "optimizer_time": raw_result.optimizer_time,
        "optimal_value": raw_result.optimal_value,
        "qubits": raw_result.optimal_circuit.width(),
        "operations_specific": dict(raw_result.optimal_circuit.decompose(reps=10).count_ops()),
        "operation_count": raw_result.optimal_circuit.decompose(reps=10).size()
    }
    print(outputobj)

    f.write(json.dumps(outputobj))

