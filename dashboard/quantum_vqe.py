#!/usr/bin/env python3
"""
Quantum VQE simulation for chemical bonding
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import os
import warnings

warnings.filterwarnings("ignore")


class FixedVQE:

    def __init__(self):

        self.J = -0.15
        self.h = 0.08
        self.c = -1.0

        self.I = np.eye(2)
        self.X = np.array([[0,1],[1,0]])
        self.Y = np.array([[0,-1],[1,0]])
        self.Z = np.array([[1,0],[0,-1]])

    def construct_hamiltonian(self):

        H = np.zeros((4,4))

        H += self.c * np.kron(self.I,self.I)
        H += self.h * np.kron(self.Z,self.I)
        H += self.h * np.kron(self.I,self.Z)

        H += self.J * np.kron(self.X,self.X)
        H += self.J * np.kron(self.Y,self.Y)
        H += self.J * np.kron(self.Z,self.Z)

        return H


    def exact_solution(self):

        H = self.construct_hamiltonian()

        eigenvalues = np.linalg.eigvalsh(H)

        return eigenvalues[0], eigenvalues


    def quantum_circuit(self,theta):

        psi = np.array([1,0,0,0])

        Ry = np.array([
            [np.cos(theta/2),-np.sin(theta/2)],
            [np.sin(theta/2), np.cos(theta/2)]
        ])

        U = np.kron(Ry,self.I)

        psi = U @ psi

        CNOT = np.array([
            [1,0,0,0],
            [0,1,0,0],
            [0,0,0,1],
            [0,0,1,0]
        ])

        psi = CNOT @ psi

        return psi


    def expectation_value(self,theta):

        psi = self.quantum_circuit(theta)

        H = self.construct_hamiltonian()

        return psi.T @ H @ psi


    def run_vqe(self,initial_theta=0.5):

        print("\n"+"="*70)
        print("VARIATIONAL QUANTUM EIGENSOLVER (VQE)")
        print("="*70)

        exact_energy,all_eigen = self.exact_solution()

        print("Exact ground state energy:",round(exact_energy,6))
        print("All eigenvalues:",[f"{e:.4f}" for e in all_eigen])

        print("Hamiltonian parameters:")
        print("  J (exchange coupling):",self.J)
        print("  h (local field):",self.h)
        print("  c (constant):",self.c)

        energies=[]
        angles=[]

        def callback(x):

            e=self.expectation_value(x[0])

            energies.append(e)
            angles.append(x[0])

            if len(energies)%5==0:
                print(f"  Step {len(energies)}: θ={x[0]:.4f}, E={e:.6f}")


        result=minimize(
            lambda x:self.expectation_value(x[0]),
            [initial_theta],
            method="COBYLA",
            callback=callback,
            options={"maxiter":50}
        )

        vqe_energy=result.fun
        optimal_theta=result.x[0]

        print("\n=== VQE RESULTS ===")
        print("Optimal parameter θ:",round(optimal_theta,6))
        print("VQE energy:",round(vqe_energy,6))
        print("Exact energy:",round(exact_energy,6))
        print("Error:",round(abs(vqe_energy-exact_energy),6))
        print("Optimization success:",result.success)
        print("Number of iterations:",result.nfev)

        self.plot_results(energies,angles,exact_energy,vqe_energy)

        return vqe_energy,optimal_theta,result


    def plot_results(self,energies,angles,exact_energy,vqe_energy):

        fig=plt.figure(figsize=(14,10))

        ax1=plt.subplot(2,3,1)
        ax1.plot(energies,"bo-",label="VQE energy")
        ax1.axhline(y=exact_energy,color="r",linestyle="--",label="Exact energy")
        ax1.axhline(y=vqe_energy,color="g",linestyle=":",label="Final VQE")
        ax1.set_title("VQE Energy Convergence")
        ax1.set_xlabel("Iteration")
        ax1.set_ylabel("Energy")
        ax1.legend()
        ax1.grid(True)


        ax2=plt.subplot(2,3,2)
        ax2.plot(angles,"gs-")
        ax2.set_title("Parameter Optimization")
        ax2.set_xlabel("Iteration")
        ax2.set_ylabel("Parameter θ (radians)")
        ax2.grid(True)


        ax3=plt.subplot(2,3,3)
        theta_range=np.linspace(0,2*np.pi,200)
        energy_land=[self.expectation_value(t) for t in theta_range]
        ax3.plot(theta_range,energy_land)
        ax3.axvline(x=angles[-1],color="r",linestyle="--",
                    label=f"Optimal θ={angles[-1]:.3f}")
        ax3.set_title("Energy Landscape")
        ax3.set_xlabel("Parameter θ (radians)")
        ax3.set_ylabel("Energy")
        ax3.legend()
        ax3.grid(True)


        ax4=plt.subplot(2,3,4)

        final_state=self.quantum_circuit(angles[-1])

        probs=final_state**2

        labels=["|00⟩","|01⟩","|10⟩","|11⟩"]

        bars=ax4.bar(labels,probs,color=["blue","green","orange","red"])

        for bar,p in zip(bars,probs):
            ax4.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.02,
                     f"{p:.3f}",ha="center")

        ax4.set_ylim(0,1)
        ax4.set_title("Final Quantum State")
        ax4.set_ylabel("Probability")


        ax5=plt.subplot(2,3,5)

        exact,all_e=self.exact_solution()

        colors=["red","blue","blue","blue"]

        ax5.bar(range(len(all_e)),all_e,color=colors)

        ax5.axhline(y=vqe_energy,color="green",linestyle="--",
                    label=f"VQE: {vqe_energy:.4f}")

        ax5.set_title("Eigenvalue Spectrum")
        ax5.set_xlabel("Eigenstate")
        ax5.set_ylabel("Energy")
        ax5.legend()


        ax6=plt.subplot(2,3,6)

        ax6.text(
            0.5,0.5,
            f"VQE Circuit: |ψ(θ)⟩ = CNOT · (Ry(θ) ⊗ I) · |00⟩\n\n"
            f"Optimal θ = {angles[-1]:.4f} rad\n"
            f"VQE Energy = {vqe_energy:.6f}\n"
            f"Exact Energy = {exact_energy:.6f}\n"
            f"Error = {abs(vqe_energy-exact_energy):.6f}",
            ha="center",
            va="center",
            bbox=dict(boxstyle="round",facecolor="wheat",alpha=0.5)
        )

        ax6.axis("off")
        ax6.set_title("Circuit & Results Summary")

        plt.tight_layout()

        os.makedirs("results",exist_ok=True)

        plt.savefig("results/vqe_results_fixed.png",dpi=300)

        print("\nResults plot saved to results/vqe_results_fixed.png")


def analyze_chemical_interpretation():

    print("\n"+"="*70)
    print("CHEMICAL INTERPRETATION OF VQE RESULTS")
    print("="*70)

    vqe=FixedVQE()

    vqe_energy,optimal_theta,result=vqe.run_vqe()

    final_state=vqe.quantum_circuit(optimal_theta)

    print("\n"+"-"*70)
    print("QUANTUM STATE → CHEMICAL BONDING")
    print("-"*70)

    states=["|00⟩","|01⟩","|10⟩","|11⟩"]

    print("\nFinal quantum state probabilities:")

    for s,p in zip(states,final_state**2):
        print(f"  {s}: {p:.4f}")

    covalent=final_state[3]**2
    ionic=final_state[1]**2+final_state[2]**2

    print("\nBOND CHARACTER ANALYSIS:")
    print("  Covalent character:",round(covalent,4))
    print("  Ionic character:",round(ionic,4))
    print("  No bond:",round(final_state[0]**2,4))

    print("\nDetailed analysis saved to results/vqe_chemical_analysis.txt")

    os.makedirs("results",exist_ok=True)

    result_text=f"""
=== VQE RESULTS ===
Optimal parameter θ: {optimal_theta:.6f}

VQE energy: {vqe_energy:.6f}
Exact energy: {vqe.exact_solution()[0]:.6f}

Error: {abs(vqe_energy-vqe.exact_solution()[0]):.6f}

Optimization success: {result.success}
Number of iterations: {result.nfev}
"""

    with open("results/quantum_vqe_final.txt","w") as f:
        f.write(result_text)



if __name__=="__main__":

    print("VQE FOR CHEMICAL BONDING SIMULATION")
    print("Quantum algorithm for molecular energy calculation")

    analyze_chemical_interpretation()

    print("\n"+"="*70)
    print("VQE SIMULATION COMPLETE")
    print("="*70)
