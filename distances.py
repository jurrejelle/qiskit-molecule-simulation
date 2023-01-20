import json

from qiskit.algorithms.minimum_eigensolvers import VQEResult, VQE
from qiskit.algorithms.optimizers import *
from qiskit.circuit.library import TwoLocal, EfficientSU2, RealAmplitudes, ExcitationPreserving
from qiskit.primitives import Estimator
from qiskit_nature.second_q.algorithms import VQEUCCFactory, GroundStateEigensolver
from qiskit_nature.second_q.circuit.library import *
from qiskit_nature.second_q.mappers import *
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
import time
import os
import numpy as np

def genh2string(dist):
    return "H 0 0 0; H 0 0 {:.4f}".format(dist)

H3 = "H 0 0 0; H 0 0 0.740848; H 0 0.641593,0.370424"
HF = "H 0 0 0; F 0 0 0.91"
HLi  = "H 0 0 0; Li 0 0 2"
CO2 = "O 0 0 0; C 0 0 1.158898; O 0 0 2.317796",
H2O = "H 0.75754079778 0.58707963658 0; O 0 0 0; H -0.75754079778 0.58707963658 0"

lines = []

start = 0.5
end = 1.7
step = 0.01

steps = int((end-start)/step) + 1

for dist in np.linspace(start, end, steps):
    energies = []
    for iterations in range(0, 5):
        driver = PySCFDriver(
            atom=genh2string(dist),
            basis="sto3g",
            charge=0,
            spin=0,
            max_memory=30760,
            unit=DistanceUnit.ANGSTROM,
        )
        problem = driver.run()


        vqe = VQEUCCFactory(Estimator(), UCCSD(), SPSA())
        converter = QubitConverter(BravyiKitaevMapper())

        calc = GroundStateEigensolver(converter, vqe)
        res = calc.solve(problem)
        energies.append(problem.interpret(res).total_energies[0].real)

    line = f"{dist:.3f}: {min(energies)}".replace(".",",")
    print(line)
    lines.append(line)

with open("distances_h2.csv", "w") as f:
    f.write("\n".join(lines))