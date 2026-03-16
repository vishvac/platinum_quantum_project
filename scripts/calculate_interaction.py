#!/usr/bin/env python3
"""
ACCURATE INTERACTION ENERGY CALCULATION
Calculates: E_interaction = E(Pt₂) - 2*E(Pt)
"""

import numpy as np
from pyscf import gto, scf
import matplotlib.pyplot as plt
import os


def calculate_pt_atom_energy():
    """Calculate single Pt atom energy accurately"""

    print("\n" + "-"*70)
    print("CALCULATING SINGLE Pt ATOM ENERGY")
    print("-"*70)

    mol = gto.Mole()
    mol.atom = 'Pt 0 0 0'
    mol.basis = 'def2svp'
    mol.ecp = 'def2svp'
    mol.spin = 2
    mol.charge = 0
    mol.verbose = 0
    mol.build()

    mf = scf.UHF(mol)
    mf.conv_tol = 1e-8
    energy = mf.kernel()

    print(f"Pt atom configuration: [Xe] 4f¹⁴ 5d⁹ 6s¹")
    print(f"Spin multiplicity: {mol.spin + 1} (triplet)")
    print(f"Number of electrons: {mol.nelectron}")
    print(f"Energy: {energy:.8f} Hartree")
    print(f"       = {energy*27.2114:.4f} eV")
    print(f"       = {energy*627.5:.2f} kcal/mol")

    return energy, mol


def calculate_pt_dimer_interaction():
    """Calculate Pt₂ dimer and interaction energy"""

    print("\n" + "-"*70)
    print("CALCULATING Pt₂ DIMER INTERACTION ENERGY")
    print("-"*70)

    # Single atom energy
    E_atom, atom_mol = calculate_pt_atom_energy()

    bond_length = 2.33

    mol = gto.Mole()
    mol.atom = f'''
    Pt 0.0 0.0 0.0
    Pt 0.0 0.0 {bond_length}
    '''
    mol.basis = 'def2svp'
    mol.ecp = 'def2svp'
    mol.spin = 0
    mol.charge = 0
    mol.verbose = 0
    mol.build()

    print(f"\nPt₂ dimer at {bond_length} Å")
    print(f"Number of electrons: {mol.nelectron}")

    mf = scf.RHF(mol)
    mf.conv_tol = 1e-8
    E_dimer = mf.kernel()

    print(f"\nDimer energy: {E_dimer:.8f} Hartree")

    E_interaction = E_dimer - 2 * E_atom

    print("\n" + "="*70)
    print("INTERACTION ENERGY RESULTS")
    print("="*70)

    print(f"E(Pt₂) = {E_dimer:.6f} Hartree")
    print(f"2 × E(Pt) = {2*E_atom:.6f} Hartree")

    print(f"\nInteraction energy ΔE = E(Pt₂) - 2E(Pt)")
    print(f"                     = {E_interaction:.6f} Hartree")
    print(f"                     = {E_interaction*27.2114:.3f} eV")
    print(f"                     = {E_interaction*627.5:.2f} kcal/mol")

    D_e = -E_interaction * 627.5
    print(f"\nBond dissociation energy Dₑ = {D_e:.2f} kcal/mol")

    # -------- SAVE FINAL RESULT FOR DASHBOARD --------

    result_text = f"""
CALCULATING SINGLE Pt ATOM ENERGY
----------------------------------------------------------------------
Pt atom configuration: [Xe] 4f¹⁴ 5d⁹ 6s¹
Spin multiplicity: {atom_mol.spin + 1} (triplet)
Number of electrons: {atom_mol.nelectron}

Pt₂ dimer at {bond_length:.2f} Å
Number of electrons: {mol.nelectron}

Dimer energy: {E_dimer:.8f} Hartree

======================================================================
INTERACTION ENERGY RESULTS
======================================================================

E(Pt₂) = {E_dimer:.6f} Hartree
2 × E(Pt) = {2*E_atom:.6f} Hartree

Interaction energy ΔE = E(Pt₂) - 2E(Pt)
                     = {E_interaction:.6f} Hartree
                     = {E_interaction*27.2114:.3f} eV
                     = {E_interaction*627.5:.2f} kcal/mol

Bond dissociation energy Dₑ = {D_e:.2f} kcal/mol
"""

    os.makedirs("results", exist_ok=True)

    with open("results/interaction_final.txt", "w") as f:
        f.write(result_text)

    return E_interaction, bond_length, D_e


def potential_energy_scan():
    """Scan potential energy surface"""

    print("\n" + "-"*70)
    print("POTENTIAL ENERGY SURFACE SCAN")
    print("-"*70)

    bond_lengths = np.linspace(2.0, 3.0, 21)
    energies = []

    for r in bond_lengths:

        mol = gto.Mole()
        mol.atom = f'''
        Pt 0.0 0.0 0.0
        Pt 0.0 0.0 {r}
        '''
        mol.basis = 'def2svp'
        mol.ecp = 'def2svp'
        mol.spin = 0
        mol.verbose = 0
        mol.build()

        mf = scf.RHF(mol)
        energy = mf.kernel()

        energies.append(energy)

    energies = np.array(energies)
    min_idx = np.argmin(energies)

    optimal_r = bond_lengths[min_idx]
    min_energy = energies[min_idx]

    # Plot curve
    plt.figure(figsize=(10,6))
    plt.plot(bond_lengths,(energies-min_energy)*627.5,'b-o')

    plt.plot(optimal_r,0,'r*',markersize=15,
             label=f'Minimum: {optimal_r:.2f} Å')

    plt.xlabel('Pt-Pt Distance (Å)')
    plt.ylabel('Relative Energy (kcal/mol)')
    plt.title('Pt₂ Potential Energy Curve')
    plt.grid(True)
    plt.legend()

    os.makedirs("results", exist_ok=True)

    plt.savefig('results/pt2_interaction_curve.png',dpi=300,bbox_inches='tight')
    plt.show()

    return optimal_r


def main():

    print("="*70)
    print("PLATINUM-PLATINUM INTERACTION ENERGY CALCULATION")
    print("="*70)

    calculate_pt_dimer_interaction()

    potential_energy_scan()

    print("\nResults saved to: results/interaction_final.txt")
    print("Graph saved to: results/pt2_interaction_curve.png")


if __name__ == "__main__":
    main()
