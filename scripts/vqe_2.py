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


    def plot_results(self, energies, angles, exact_energy, vqe_energy):
        """Plot VQE results with corrected eigenvalue spectrum"""
        
        fig = plt.figure(figsize=(14, 10))
        
        # 1. VQE Energy Convergence
        ax1 = plt.subplot(2, 3, 1)
        ax1.plot(energies, "bo-", label="VQE energy")
        ax1.axhline(y=exact_energy, color="r", linestyle="--", label="Exact energy")
        ax1.axhline(y=vqe_energy, color="g", linestyle=":", label="Final VQE")
        ax1.set_title("VQE Energy Convergence")
        ax1.set_xlabel("Iteration")
        ax1.set_ylabel("Energy")
        ax1.legend()
        ax1.grid(True)
        
        # 2. Parameter Optimization
        ax2 = plt.subplot(2, 3, 2)
        ax2.plot(angles, "gs-")
        ax2.set_title("Parameter Optimization")
        ax2.set_xlabel("Iteration")
        ax2.set_ylabel("Parameter θ (radians)")
        ax2.grid(True)
        
        # 3. Energy Landscape
        ax3 = plt.subplot(2, 3, 3)
        theta_range = np.linspace(0, 2*np.pi, 200)
        energy_land = [self.expectation_value(t) for t in theta_range]
        ax3.plot(theta_range, energy_land)
        ax3.axvline(x=angles[-1], color="r", linestyle="--",
                    label=f"Optimal θ={angles[-1]:.3f}")
        ax3.set_title("Energy Landscape")
        ax3.set_xlabel("Parameter θ (radians)")
        ax3.set_ylabel("Energy")
        ax3.legend()
        ax3.grid(True)
        
        # 4. Final Quantum State
        ax4 = plt.subplot(2, 3, 4)
        final_state = self.quantum_circuit(angles[-1])
        probs = final_state**2
        labels = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"]
        bars = ax4.bar(labels, probs, color=["blue", "green", "orange", "red"])
        for bar, p in zip(bars, probs):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                     f"{p:.3f}", ha="center")
        ax4.set_ylim(0, 1)
        ax4.set_title("Final Quantum State")
        ax4.set_ylabel("Probability")
        
        # 5. CORRECTED Eigenvalue Spectrum
        ax5 = plt.subplot(2, 3, 5)
        
        # Get ALL eigenvalues and sort them
        exact, all_e = self.exact_solution()
        all_e_sorted = np.sort(all_e)
        n_states = len(all_e_sorted)
        
        # Plot energy levels as horizontal lines (correct representation)
        for i, energy in enumerate(all_e_sorted):
            # Ground state in red, excited states in blue
            color = 'red' if i == 0 else 'blue'
            linewidth = 3 if i == 0 else 2
            
            # Draw horizontal line for each eigenvalue
            ax5.hlines(y=energy, xmin=i-0.3, xmax=i+0.3, 
                       color=color, linewidth=linewidth)
            
            # Add energy value label
            ax5.text(i, energy + 0.02, f'{energy:.4f}', 
                    ha='center', fontsize=9)
            
            # Add state label
            if i == 0:
                state_label = f'E{i}\n(Ground)'
            else:
                state_label = f'E{i}\n(Excited)'
            ax5.text(i, min(all_e_sorted) - 0.15, state_label,
                    ha='center', fontsize=8)
        
        # Mark VQE result - it should match ground state energy
        ax5.plot(0, vqe_energy, 'g*', markersize=15, 
                 label=f'VQE: {vqe_energy:.4f}')
        
        # Add energy gaps annotation
        for i in range(len(all_e_sorted)-1):
            gap = all_e_sorted[i+1] - all_e_sorted[i]
            mid_energy = (all_e_sorted[i] + all_e_sorted[i+1]) / 2
            
            # Draw arrow for gap
            ax5.annotate('', xy=(i+0.4, all_e_sorted[i]), 
                        xytext=(i+0.4, all_e_sorted[i+1]),
                        arrowprops=dict(arrowstyle='<->', color='gray'))
            
            # Add gap value
            ax5.text(i+0.5, mid_energy, f'{gap:.4f}', 
                    fontsize=8, color='gray', ha='left')
        
        # Formatting
        ax5.set_xlim(-0.5, n_states - 0.5)
        ax5.set_xticks(range(n_states))
        ax5.set_xticklabels([f'State {i}' for i in range(n_states)])
        ax5.set_ylabel('Energy')
        ax5.set_title('Eigenvalue Spectrum ')
        ax5.legend(loc='best')
        ax5.grid(True, axis='y', alpha=0.3)
        
        # 6. CORRECTED Results Summary with Table
        ax6 = plt.subplot(2, 3, 6)
        
        # Calculate energy gaps
        gap1 = all_e_sorted[1] - all_e_sorted[0]
        gap2 = all_e_sorted[2] - all_e_sorted[1]
        gap3 = all_e_sorted[3] - all_e_sorted[2]
        
        # Create a proper table of results
        table_data = [
            ['Parameter', 'Value'],
            ['Optimal θ', f'{angles[-1]:.4f} rad'],
            ['VQE Energy', f'{vqe_energy:.6f}'],
            ['Exact Energy', f'{exact_energy:.6f}'],
            ['Error', f'{abs(vqe_energy-exact_energy):.6f}'],
            ['E0 (Ground)', f'{all_e_sorted[0]:.6f}'],
            ['E1 (Excited)', f'{all_e_sorted[1]:.6f}'],
            ['E2 (Excited)', f'{all_e_sorted[2]:.6f}'],
            ['E3 (Excited)', f'{all_e_sorted[3]:.6f}'],
            ['Gap E1-E0', f'{gap1:.6f}'],
            ['Gap E2-E1', f'{gap2:.6f}'],
            ['Gap E3-E2', f'{gap3:.6f}']
        ]
        
        # Create table in matplotlib
        table = ax6.table(cellText=table_data, loc='center',
                          cellLoc='left', colWidths=[0.25, 0.25])
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.2)
        
        ax6.axis('off')
        ax6.set_title('VQE Results Summary')
        
        plt.tight_layout()
        
        os.makedirs("results", exist_ok=True)
        plt.savefig("results/vqe_results_fixed.png", dpi=300)
        print("\n✓ Results plot saved to results/vqe_results_fixed.png")


def analyze_chemical_interpretation():

    print("\n"+"="*70)
    print("CHEMICAL INTERPRETATION OF VQE RESULTS")
    print("="*70)

    vqe = FixedVQE()

    vqe_energy, optimal_theta, result = vqe.run_vqe()

    final_state = vqe.quantum_circuit(optimal_theta)

    print("\n"+"-"*70)
    print("QUANTUM STATE → CHEMICAL BONDING")
    print("-"*70)

    states = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"]

    print("\nFinal quantum state probabilities:")

    for s, p in zip(states, final_state**2):
        print(f"  {s}: {p:.4f}")

    covalent = final_state[3]**2
    ionic = final_state[1]**2 + final_state[2]**2

    print("\nBOND CHARACTER ANALYSIS:")
    print("  Covalent character:", round(covalent, 4))
    print("  Ionic character:", round(ionic, 4))
    print("  No bond:", round(final_state[0]**2, 4))

    print("\nDetailed analysis saved to results/vqe_chemical_analysis.txt")

    os.makedirs("results", exist_ok=True)

    # CORRECTED: Get full eigenvalue spectrum for output
    exact, all_e = vqe.exact_solution()
    all_e_sorted = np.sort(all_e)
    
    # Calculate gaps
    gap1 = all_e_sorted[1] - all_e_sorted[0]
    gap2 = all_e_sorted[2] - all_e_sorted[1]
    gap3 = all_e_sorted[3] - all_e_sorted[2]

    result_text = f"""
=== VQE RESULTS ===
Optimal parameter θ: {optimal_theta:.6f}

VQE energy: {vqe_energy:.6f}
Exact energy: {exact:.6f}
Error: {abs(vqe_energy - exact):.6f}

=== EIGENVALUE SPECTRUM ===
Ground state (E0): {all_e_sorted[0]:.6f}
1st Excited (E1):  {all_e_sorted[1]:.6f}
2nd Excited (E2):  {all_e_sorted[2]:.6f}
3rd Excited (E3):  {all_e_sorted[3]:.6f}

Energy gaps:
E1 - E0 = {gap1:.6f}
E2 - E1 = {gap2:.6f}
E3 - E2 = {gap3:.6f}

Optimization success: {result.success}
Number of iterations: {result.nfev}


=== BONDING ANALYSIS ===
Covalent character: {covalent:.4f}
Ionic character: {ionic:.4f}
No bond: {final_state[0]**2:.4f}
"""

    with open("results/quantum_vqe_final.txt", "w") as f:
        f.write(result_text)
    
    print("\n✓ Results saved to results/quantum_vqe_final.txt")


if __name__ == "__main__":

    print("="*70)
    print("VQE FOR CHEMICAL BONDING SIMULATION")
    print("Quantum algorithm for molecular energy calculation")
    print("="*70)

    analyze_chemical_interpretation()

    print("\n"+"="*70)
    print("VQE SIMULATION COMPLETE")
    print("="*70)
