from qiskit.algorithms.minimum_eigensolvers import NumPyMinimumEigensolver
from qiskit.algorithms.optimizers import *
from qiskit.primitives import Estimator
from qiskit_nature.second_q.algorithms import VQEUCCFactory, GroundStateEigensolver
from qiskit_nature.second_q.circuit.library import *
from qiskit_nature.second_q.mappers import *
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
import numpy as np
import math



def genh2string(dist):
    return "H 0 0 0; H 0 0 {:.4f}".format(dist)

def genhlistring(dist):
    return "H 0 0 0; Li 0 0 {:.4f}".format(dist)

# Angle between bonds = 104,5 deg
# Turn first particle by 90-52.25 deg
# Turn second particle by 90+52.25 deg
def genh2ostring(dist):
    return "H 0 {:.4f} {:.4f}; O 0 0 0; H 0 {:.4f} {:.4f}".format(dist * math.sin(math.radians(90-52.25)),
                                                                  dist * math.cos(math.radians(90-52.25)),
                                                                  dist * math.sin(math.radians(90+52.25)),
                                                                  dist * math.cos(math.radians(90+52.25)))


# Assuming h3 is an equilateral triangle
def genh3string(dist):
    return "H 0 0 0; H 0 0 {:.4f}; H 0 {:.4f} {:.4f}".format(dist,
                                                             dist * math.sin(math.pi/3),
                                                             dist * math.cos(math.pi/3))
MOLECULE = "h2o"
lines = []

if MOLECULE == "h2":
    start = 0.5
    end = 1.7
    step = 0.01
elif MOLECULE == "h3":
    start = 0.1
    end = 2
    step = 0.05
elif MOLECULE == "hli":
    start = 0.1
    end = 1.4
    step = 0.025
elif MOLECULE == "h2o":
    start = 0.7
    end = 1.6
    step = 0.01


steps = int((end-start)/step) + 1

for dist in np.linspace(start, end, steps):
    energies = []
    for iterations in range(0, 2):
        driver = None
        if MOLECULE == "h3":

            driver = PySCFDriver(
                atom= genh3string(dist),
                basis="sto3g",
                charge=0,
                spin=1,
                max_memory=30760,
                unit=DistanceUnit.ANGSTROM,
            )
        elif MOLECULE == "h2":

            driver = PySCFDriver(
                atom= genh2string(dist),
                basis="sto3g",
                charge=0,
                spin=0,
                max_memory=30760,
                unit=DistanceUnit.ANGSTROM,
            )
        elif MOLECULE == "hli":

            driver = PySCFDriver(
                atom=genhlistring(dist),
                basis="sto3g",
                charge=0,
                spin=0,
                max_memory=30760,
                unit=DistanceUnit.ANGSTROM,
            )
        elif MOLECULE == "h2o":

            driver = PySCFDriver(
                atom= genh2ostring(dist),
                basis="sto3g",
                charge=0,
                spin=0,
                max_memory=30760,
                unit=DistanceUnit.ANGSTROM,
            )

        problem = driver.run()

        vqe = VQEUCCFactory(Estimator(), UCCSD(), SPSA())
        converter = QubitConverter(BravyiKitaevMapper())
        if MOLECULE == 'hli' or MOLECULE == "h2o":
            vqe = NumPyMinimumEigensolver()
        calc = GroundStateEigensolver(converter, vqe)
        res = calc.solve(problem)
        energies.append(problem.interpret(res).total_energies[0].real)

    line = f"{dist:.3f}: {min(energies)}".replace(".",",")
    print(line)
    lines.append(line)

with open(f"distances_{MOLECULE}.csv", "w") as f:
    f.write("\n".join(lines))