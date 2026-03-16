#!/usr/bin/env python3

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.mappers import JordanWignerMapper
import os

print("\n" + "="*60)
print("MOLECULE → QUBIT HAMILTONIAN CONVERSION")
print("="*60)

# Define molecule (example H2)
driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.74",
    basis="sto3g",
    unit=DistanceUnit.ANGSTROM
)

# Run classical chemistry driver
problem = driver.run()

# Get fermionic Hamiltonian
second_q_op = problem.hamiltonian.second_q_op()

print("\nFermionic Hamiltonian:")
print(second_q_op)

# Convert fermionic → qubit Hamiltonian
mapper = JordanWignerMapper()

qubit_hamiltonian = mapper.map(second_q_op)

print("\nQubit Hamiltonian:")
print(qubit_hamiltonian)

# -------- SAVE FINAL RESULT FOR DASHBOARD --------

result_text = f"""
Qubit Hamiltonian:

{qubit_hamiltonian}
"""

os.makedirs("results", exist_ok=True)

with open("results/molecule_qubit_final.txt", "w") as f:
    f.write(result_text)

print("\nResult saved to: results/molecule_qubit_final.txt")
