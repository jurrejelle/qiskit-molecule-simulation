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

mappers = [
   BravyiKitaevMapper,
   BravyiKitaevSuperFastMapper,
   JordanWignerMapper,
   ParityMapper
]

ansatzes = [
   UCCSD(),
   RealAmplitudes(2),
   TwoLocal(2, "ry", "cz"),
   EfficientSU2(2, reps=3, entanglement='full'),
   ExcitationPreserving(2, mode='iswap', entanglement='full')
]


optimizers = [
   ADAM,
   AQGD,
   CG,
   COBYLA,
   L_BFGS_B,
   GSLS,
   GradientDescent,
#   GradientDescentState, Takes 8 parameters, probably only works if you want a specific initial state
   NELDER_MEAD,
   NFT,
   P_BFGS,
   POWELL,
   SLSQP,
   SPSA,
#   QNSPSA, Takes initial argument "fidelity". Need to calculate this per sansatz with sampler, which seems annoying
   TNC,
#   SciPyOptimizer, Takes initial argument "method". This is just scipy running any of the other given optimizers
   UMDA
]


H2  = "H 0 0 0; H 0 0 0.740848"
H3 = "H 0 0 0; H 0 0 0.740848; H 0 0.641593,0.370424"
HF = "H 0 0 0; F 0 0 0.91"
HLi  = "H 0 0 0; Li 0 0 2"
CO2 = "O 0 0 0; C 0 0 1.158898; O 0 0 2.317796",
H2O = "H 0.75754079778 0.58707963658 0; O 0 0 0; H -0.75754079778 0.58707963658 0"
outputfile = "output_h2.json"
if outputfile not in os.listdir():
    with open(outputfile, "w") as f:
        f.write("[]")
if "not_working.json" not in os.listdir():
    with open("not_working.json", "w") as f:
        f.write("[]")


for mapper in mappers:
    for ansatz in ansatzes:
        for optimizer in optimizers:

            ident = f"{mapper.__name__}, {ansatz.__class__.__name__}, {optimizer.__name__}"
            driver = PySCFDriver(
                atom=H2,
                basis="sto3g",
                charge=0,
                spin=0,
                max_memory=30760,
                unit=DistanceUnit.ANGSTROM,
            )
            problem = driver.run()

            def callback_fun(count, parameters, mean, metadata):
                global beforetime, ident
                newtime = time.time()
                if newtime - beforetime > 600:
                    print(ident+"Took too long")
                    raise Exception("took too long")
#                print(f"Iteration: {count}\nParameters: {parameters}\nMean: {mean}\n\n")


            try:
                try:
                    vqe = VQEUCCFactory(Estimator(), ansatz, optimizer(), callback=callback_fun)
                    converter = QubitConverter(mapper(), two_qubit_reduction=True)

                    calc = GroundStateEigensolver(converter, vqe)
                    beforetime = time.time()
                    res = calc.solve(problem)
                except Exception as e:
                    try:
                        vqe = VQE(Estimator(), ansatz, optimizer(), callback=callback_fun)
                        converter = QubitConverter(mapper())

                        calc = GroundStateEigensolver(converter, vqe)
                        beforetime = time.time()
                        res = calc.solve(problem)
                    except Exception as e2:
                        raise Exception(str(e) + str(e2))
            except Exception as e:
                print(ident+", "+str(e))

                with open("not_working.json", "r") as f:
                    nw = json.loads(f.read())
                nw.append(ident)
                with open("not_working.json", "w") as f:
                    f.write(json.dumps(nw))
                continue

            print(f"{'='*20}{ident}{'='*20}")
            aftertime = time.time()
            time_taken = aftertime - beforetime
            if not isinstance(res.raw_result, VQEResult):
                with open("not_working.json", "r") as f:
                    nw = json.loads(f.read())
                nw.append(ident)
                with open("not_working.json", "w") as f:
                    f.write(json.dumps(nw))
                continue

            raw_result: VQEResult = res.raw_result
            result_object = {
                "mapper": mapper.__name__,
                "ansatz": ansatz.__class__.__name__,
                "optimizer": optimizer.__name__,
                "time": time_taken,
                "optimal_value": raw_result.optimal_value,
                "eigenvalue": raw_result.eigenvalue,
                "optimizer_time": raw_result.optimizer_time,
                "qubits":res.raw_result.optimal_circuit.width(),
                "operations_specific":res.raw_result.optimal_circuit.decompose(reps=10).count_ops(),
                "operation_count":res.raw_result.optimal_circuit.decompose(reps=10).size()
            }
            try:
                qasmstring = res.raw_result.optimal_circuit.qasm()
                result_object["qasmstring"] = qasmstring
            except:
                pass

            print(result_object)

            with open(outputfile, "r") as f:
                output = json.loads(f.read())
            output.append(result_object)
            with open(outputfile, "w") as f:
                f.write(json.dumps(output))
