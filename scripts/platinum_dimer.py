#!/usr/bin/env python3
"""
CORRECT PLATINUM DIMER CALCULATION
Pt-Pt interaction study
"""

import numpy as np
from pyscf import gto, scf
import matplotlib.pyplot as plt
import os
import datetime


def calculate_pt2_potential_curve():
    """Calculate Pt₂ potential energy curve"""
    
    print("\n" + "="*70)
    print("PLATINUM DIMER POTENTIAL ENERGY CURVE")
    print("="*70)
    
    bond_lengths = np.linspace(2.0, 3.0, 11)

    energies_singlet = []
    energies_triplet = []

    for r in bond_lengths:
        print(f"\nBond length: {r:.2f} Å")

        mol = gto.Mole()
        mol.atom = f'''
        Pt 0.0 0.0 0.0
        Pt 0.0 0.0 {r}
        '''
        mol.basis = 'def2svp'
        mol.ecp = 'def2svp'
        mol.verbose = 0

        mol.spin = 0
        mol.build()

        mf_singlet = scf.RHF(mol)
        energy_singlet = mf_singlet.kernel()
        energies_singlet.append(energy_singlet)

        print(f"  Singlet: {energy_singlet:.6f} Hartree")

        mol.spin = 2
        mol.build()

        mf_triplet = scf.UHF(mol)
        energy_triplet = mf_triplet.kernel()
        energies_triplet.append(energy_triplet)

        print(f"  Triplet: {energy_triplet:.6f} Hartree")

    bond_lengths = np.array(bond_lengths)
    energies_singlet = np.array(energies_singlet)
    energies_triplet = np.array(energies_triplet)

    min_energy = min(np.min(energies_singlet), np.min(energies_triplet))

    rel_singlet = (energies_singlet - min_energy) * 627.5
    rel_triplet = (energies_triplet - min_energy) * 627.5

    opt_singlet_idx = np.argmin(rel_singlet)
    opt_triplet_idx = np.argmin(rel_triplet)

    print("\n" + "-"*70)
    print("RESULTS:")
    print(f"Optimal singlet bond length: {bond_lengths[opt_singlet_idx]:.3f} Å")
    print(f"Optimal triplet bond length: {bond_lengths[opt_triplet_idx]:.3f} Å")
    print(f"Singlet binding energy: {-rel_singlet[opt_singlet_idx]:.2f} kcal/mol")
    print(f"Triplet binding energy: {-rel_triplet[opt_triplet_idx]:.2f} kcal/mol")

    plt.figure(figsize=(12, 8))

    plt.plot(bond_lengths, rel_singlet, 'b-o', linewidth=2, markersize=8,
             label='Singlet')
    plt.plot(bond_lengths, rel_triplet, 'r-s', linewidth=2, markersize=8,
             label='Triplet')

    plt.plot(bond_lengths[opt_singlet_idx], rel_singlet[opt_singlet_idx],
             'b*', markersize=15,
             label=f'Singlet min: {bond_lengths[opt_singlet_idx]:.2f} Å')

    plt.plot(bond_lengths[opt_triplet_idx], rel_triplet[opt_triplet_idx],
             'r*', markersize=15,
             label=f'Triplet min: {bond_lengths[opt_triplet_idx]:.2f} Å')

    plt.xlabel('Bond Length (Å)', fontsize=14)
    plt.ylabel('Relative Energy (kcal/mol)', fontsize=14)
    plt.title('Pt₂ Dimer Potential Energy Curves', fontsize=16)

    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)

    os.makedirs('results', exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    plt.savefig(f'results/pt2_pes_{timestamp}.png', dpi=300, bbox_inches='tight')

    plt.show()

    np.savez(f'results/pt2_data_{timestamp}.npz',
             bond_lengths=bond_lengths,
             energies_singlet=energies_singlet,
             energies_triplet=energies_triplet,
             rel_singlet=rel_singlet,
             rel_triplet=rel_triplet)

    return bond_lengths, energies_singlet, energies_triplet


def analyze_bonding_at_optimum():
    """Analyze bonding at optimal geometry"""

    print("\n" + "="*70)
    print("BONDING ANALYSIS AT OPTIMAL GEOMETRY")
    print("="*70)

    r_opt = 2.33

    mol = gto.Mole()
    mol.atom = f'''
    Pt 0.0 0.0 0.0
    Pt 0.0 0.0 {r_opt}
    '''

    mol.basis = 'def2svp'
    mol.ecp = 'def2svp'
    mol.spin = 0
    mol.verbose = 4

    mol.build()

    print(f"\nPt₂ dimer at {r_opt} Å")
    print(f"Number of electrons: {mol.nelectron}")
    print(f"Basis functions: {mol.nao}")

    mf = scf.RHF(mol)

    mf.conv_tol = 1e-8

    energy = mf.kernel()

    print(f"\nTotal energy: {energy:.6f} Hartree")
    print(f"            = {energy*627.5:.2f} kcal/mol")

    mo_energy = mf.mo_energy
    mo_occ = mf.mo_occ

    homo_idx = np.where(mo_occ > 0.5)[0][-1]
    lumo_idx = np.where(mo_occ < 0.5)[0][0]

    print(f"\nFrontier orbitals:")
    print(f"HOMO (orbital {homo_idx+1}): {mo_energy[homo_idx]:.6f} Hartree")
    print(f"                   {mo_energy[homo_idx]*27.2114:.3f} eV")

    print(f"LUMO (orbital {lumo_idx+1}): {mo_energy[lumo_idx]:.6f} Hartree")
    print(f"                   {mo_energy[lumo_idx]*27.2114:.3f} eV")

    print(f"HOMO-LUMO gap: {(mo_energy[lumo_idx]-mo_energy[homo_idx])*27.2114:.3f} eV")

    s = mol.intor('int1e_ovlp')

    dm = mf.make_rdm1()

    bond_pop = np.einsum('ij,ji->',
                         dm[:mol.nao//2, mol.nao//2:],
                         s[:mol.nao//2, mol.nao//2:])

    print(f"\nMulliken bond population: {bond_pop:.4f}")

    # -------- SAVE FINAL RESULT FOR DASHBOARD --------

    result_text = f"""
converged SCF energy = {mf.e_tot}

Total energy: {energy:.6f} Hartree
             = {energy*627.5:.2f} kcal/mol

Frontier orbitals:
HOMO (orbital {homo_idx+1}): {mo_energy[homo_idx]:.6f} Hartree
                   {mo_energy[homo_idx]*27.2114:.3f} eV
LUMO (orbital {lumo_idx+1}): {mo_energy[lumo_idx]:.6f} Hartree
                   {mo_energy[lumo_idx]*27.2114:.3f} eV

HOMO-LUMO gap: {(mo_energy[lumo_idx]-mo_energy[homo_idx])*27.2114:.3f} eV

Mulliken bond population: {bond_pop:.4f}
"""

    os.makedirs("results", exist_ok=True)

    with open("results/dimer_final.txt", "w") as f:
        f.write(result_text)

    return mf, mol


def main():
    """Main function"""

    print("\n" + "="*70)
    print("PLATINUM DIMER INTERACTION STUDY")
    print("="*70)

    calculate_pt2_potential_curve()

    analyze_bonding_at_optimum()

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)


if __name__ == "__main__":
    main()
