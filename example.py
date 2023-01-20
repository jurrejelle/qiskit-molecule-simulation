from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import Estimator
from qiskit_nature.second_q.algorithms import GroundStateEigensolver, VQEUCCFactory
from qiskit_nature.second_q.circuit.library import *
from qiskit_nature.second_q.mappers import QubitConverter, JordanWignerMapper
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver


H2  = "H 0 0 0; H 0 0 0.740848"
He2 = "He 0. 0. 0.; He 3.1 0. 0"
HLi  = "H 0 0 0; Li 0 0 2"
CO2 = "O 0 0 0; C 0 0 1.158898; O 0 0 2.317796",
H2O = "H 0.75754079778 0.58707963658 0; O 0 0 0; H -0.75754079778 0.58707963658 0"

driver = PySCFDriver(
    atom=H2,
    basis="sto3g",
    charge=0,
    spin=0,
    max_memory=30760,
    unit=DistanceUnit.ANGSTROM,
)
problem = driver.run()

# Works:
vqe_solver = VQEUCCFactory(Estimator(), UCCSD(), SLSQP())

# Doesn't work:
#vqe_solver = VQEUCCFactory(Estimator(), UCC(), SLSQP())

# Works with non-UCC examples
#ansatz = TwoLocal(2, ['ry', 'rx'], "cz")
#vqe_solver = VQE(Estimator(), ansatz, SLSQP())

converter = QubitConverter(JordanWignerMapper())

calc = GroundStateEigensolver(converter, vqe_solver)
res = calc.solve(problem)
print(res)