from qiskit.algorithms.minimum_eigensolvers import NumPyMinimumEigensolver
from qiskit.algorithms.optimizers import SLSQP
from qiskit.primitives import Estimator
from qiskit_nature.second_q.algorithms import VQEUCCFactory, GroundStateEigensolver
from qiskit_nature.second_q.circuit.library import UCCSD
from qiskit_nature.second_q.mappers import QubitConverter, JordanWignerMapper
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver


H2  = "H 0 0 0; H 0 0 0.740848"
HLi  = "H 0 0 0; Li 0 0 2"
CO2 = "O 0 0 0; C 0 0 1.158898; O 0 0 2.317796"
H2O = "H 0.75754079778 0.58707963658 0; O 0 0 0; H -0.75754079778 0.58707963658 0"
H3 = "H 0 0 0; H 0 0 0.740848; H 0 0.641593,0.370424"

driver = PySCFDriver(
    atom=H3,
    basis="sto3g",
    charge=0,
    spin=0,
    max_memory=30760,
    unit=DistanceUnit.ANGSTROM,
)
problem = driver.run()

data = ""
def callback_fun(count, parameters, mean, metadata):
    global data
    curr = f"Iteration: {count}\nParameters: {parameters}\nMean: {mean}\n\n"
    data += curr
    print(curr)

vqe_solver = VQEUCCFactory(Estimator(), UCCSD(), SLSQP(), callback=callback_fun)
converter = QubitConverter(JordanWignerMapper())
numpy_solver = NumPyMinimumEigensolver()

calc = GroundStateEigensolver(converter, numpy_solver)
res = calc.solve(problem)
print(res)
input("press any key to continue")
print(data)
input("press any key to continue")
#print(res.raw_result.optimal_circuit.decompose())

for i in range(0, 10):
    print(f"{'='*10}Iteration {i}{'='*10}'")
    print(vqe_solver.minimum_eigensolver.ansatz.decompose(reps=i))