from qiskit_nature.mappers.second_quantization import FermionicMapper
from qiskit_nature.second_q.mappers import *

__all__ = [
    "BravyiKitaevMapper",
    "BravyiKitaevSuperFastMapper",
    "DirectMapper",
    "JordanWignerMapper",
    "ParityMapper",
    "LinearMapper",
    "LogarithmicMapper",
    "QubitConverter",
    "QubitMapper",
]
a = __import__("qiskit_nature.second_q.mappers", globals(), locals(), __all__, 0)
for className in __all__:
    myClass = getattr(a, className)
    print(isinstance(myClass, FermionicMapper))