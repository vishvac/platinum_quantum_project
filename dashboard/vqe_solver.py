#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import os

from qiskit.primitives import StatevectorEstimator as Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms import NumPyMinimumEigensolver
from qiskit.circuit.library import TwoLocal

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.mappers import JordanWignerMapper


print("\n" + "="*60)
print("VARIATIONAL QUANTUM EIGENSOLVER (VQE)")
print("="*60)


# -------------------------------------------------
# STEP 1: Generate Molecular Hamiltonian
# -------------------------------------------------

driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.74",
    basis="sto3g",
    unit=DistanceUnit.ANGSTROM
)

problem = driver.run()

second_q_op = problem.hamiltonian.second_q_op()

mapper = JordanWignerMapper()

qubit_hamiltonian = mapper.map(second_q_op)

print("\nQubit Hamiltonian:")
print(qubit_hamiltonian)


# -------------------------------------------------
# STEP 2: Build Quantum Circuit Ansatz
# -------------------------------------------------

ansatz = TwoLocal(
    rotation_blocks="ry",
    entanglement_blocks="cz",
    reps=2
)


# -------------------------------------------------
# STEP 3: Setup Optimizer and Estimator
# -------------------------------------------------

optimizer = COBYLA(maxiter=100)

estimator = Estimator()


# -------------------------------------------------
# STEP 4: Track VQE Energy Convergence
# -------------------------------------------------

energies = []

def callback(eval_count, parameters, mean, std):
    energies.append(mean)


# -------------------------------------------------
# STEP 5: Run VQE Algorithm
# -------------------------------------------------

vqe = VQE(
    estimator,
    ansatz,
    optimizer,
    callback=callback
)

result = vqe.compute_minimum_eigenvalue(qubit_hamiltonian)

vqe_energy = result.eigenvalue.real

print("\nVQE Ground State Energy:", vqe_energy)


# -------------------------------------------------
# STEP 6: Exact Classical Solution
# -------------------------------------------------

exact_solver = NumPyMinimumEigensolver()

exact_result = exact_solver.compute_minimum_eigenvalue(qubit_hamiltonian)

exact_energy = exact_result.eigenvalue.real

error = abs(exact_energy - vqe_energy)

print("\nExact Energy:", exact_energy)
print("VQE Energy:", vqe_energy)
print("Error:", error)


# -------------------------------------------------
# STEP 7: Plot Energy Convergence
# -------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(energies, marker='o')

plt.axhline(y=exact_energy, color='r', linestyle='--', label="Exact Energy")

plt.xlabel("Iteration")
plt.ylabel("Energy")
plt.title("VQE Energy Convergence")

plt.legend()
plt.grid()

os.makedirs("results", exist_ok=True)

plt.savefig("results/vqe_convergence.png", dpi=300, bbox_inches="tight")

plt.show()


# -------------------------------------------------
# SAVE FINAL RESULT FOR DASHBOARD
# -------------------------------------------------

result_text = f"""
VQE Ground State Energy: {vqe_energy}

Exact Energy: {exact_energy}
VQE Energy: {vqe_energy}
Error: {error}
"""

with open("results/vqe_final.txt","w") as f:
    f.write(result_text)

print("\nResults saved to results/vqe_final.txt")
