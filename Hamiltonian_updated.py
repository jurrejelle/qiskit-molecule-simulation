from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.algorithms import GroundStateEigensolver, NumPyMinimumEigensolverFactory
from qiskit_nature.second_q.mappers import JordanWignerMapper, QubitConverter

driver = PySCFDriver(
#    atom="H 0 0 0; H 0 0 1.40; H 0 1.40 0; H 1.40 0 0",
    atom="H 0 0 0; Li 0 0 3.7794519772 ",
    basis="sto3g",
    charge=0,
    spin=0,
    unit=DistanceUnit.BOHR,
)
problem = driver.run()
print(problem.hamiltonian)
print(type(problem.second_q_ops()))
mapper = JordanWignerMapper()
converter = QubitConverter(mapper)


print(problem.molecule)
exit()
solver = GroundStateEigensolver(
    converter,
    NumPyMinimumEigensolverFactory(),
)
print(mapper.sparse_pauli_operators(2))
result = solver.solve(problem)

#print(result)

#print(JordanWignerMapper().pauli_table(2))