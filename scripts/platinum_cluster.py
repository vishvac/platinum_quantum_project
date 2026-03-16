#!/usr/bin/env python3
"""
PLATINUM TETRAMER CLUSTER (Pt₄)
Important for catalysis - models nanoparticle surfaces
"""

import numpy as np
from pyscf import gto, scf, dft
from pyscf.data.elements import ELEMENTS_PROTON
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os


def create_pt4_tetrahedron():
    """Create tetrahedral Pt₄ cluster"""

    print("\n" + "="*70)
    print("PLATINUM TETRAMER CLUSTER (TETRAHEDRAL)")
    print("="*70)

    r = 2.7

    coords = [
        [0.0, 0.0, 0.0],
        [r, 0.0, 0.0],
        [r/2, r*np.sqrt(3)/2, 0.0],
        [r/2, r*np.sqrt(3)/6, r*np.sqrt(2/3)]
    ]

    mol = gto.Mole()
    mol.atom = []

    for coord in coords:
        mol.atom.append(['Pt', coord])

    mol.basis = 'def2svp'
    mol.ecp = 'def2svp'
    mol.spin = 0
    mol.charge = 0
    mol.verbose = 4
    mol.build()

    print(f"Pt₄ tetrahedron created:")
    print(f"  Number of atoms: {len(mol.atom)}")
    print(f"  Number of electrons: {mol.nelectron}")
    print(f"  Bond length: {r} Å")

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    for i, coord in enumerate(coords):
        ax.scatter(coord[0], coord[1], coord[2], s=500, c='blue')

    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            ax.plot([coords[i][0],coords[j][0]],
                    [coords[i][1],coords[j][1]],
                    [coords[i][2],coords[j][2]], 'gray', alpha=0.5)

    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlabel('Z (Å)')
    ax.set_title('Pt₄ Tetrahedral Cluster')

    os.makedirs("results", exist_ok=True)

    plt.savefig('results/pt4_cluster.png', dpi=300, bbox_inches='tight')
    plt.show()

    return mol


def calculate_pt4_cluster():
    """Calculate Pt₄ cluster properties"""

    mol = create_pt4_tetrahedron()

    print("\nRunning DFT calculation (PBE0 functional)...")

    mf = dft.RKS(mol)
    mf.xc = 'pbe0'
    mf.conv_tol = 1e-7
    mf.max_cycle = 200

    energy = mf.kernel()

    print(f"\nResults:")
    print(f"  Total energy: {energy:.6f} Hartree")
    print(f"  Energy per atom: {energy/4:.6f} Hartree")

    pt_atom = gto.Mole()
    pt_atom.atom = 'Pt 0 0 0'
    pt_atom.basis = 'def2svp'
    pt_atom.ecp = 'def2svp'
    pt_atom.spin = 2
    pt_atom.build()

    mf_atom = scf.UHF(pt_atom)
    atom_energy = mf_atom.kernel()

    cohesive_energy_per_atom = (energy - 4*atom_energy) / 4

    print(f"  Cohesive energy per atom: {cohesive_energy_per_atom:.6f} Hartree")
    print(f"                        = {cohesive_energy_per_atom*627.5:.2f} kcal/mol")

    mo_energy = mf.mo_energy
    mo_occ = mf.mo_occ

    homo_idx = np.where(mo_occ > 0.5)[0][-1]
    lumo_idx = np.where(mo_occ < 0.5)[0][0]

    gap = (mo_energy[lumo_idx] - mo_energy[homo_idx]) * 27.2114

    print(f"  HOMO-LUMO gap: {gap:.3f} eV")

    dm = mf.make_rdm1()
    s = mol.intor_symmetric('int1e_ovlp')
    mulliken = np.einsum('ij,ji->i', dm, s)

    charges = []

    print("\nMulliken charges per atom:")
    for i in range(len(mol.atom)):
        charge = 78 - mulliken[i]
        charges.append(charge)
        print(f"  Pt{i+1}: {charge:.4f}")

    # -------- SAVE FINAL RESULT FOR DASHBOARD --------

    result_text = f"""
converged SCF energy = {mf.e_tot}

Results:
Total energy: {energy:.6f} Hartree
Energy per atom: {energy/4:.6f} Hartree

converged SCF energy = {mf.e_tot}   <S^2> = {mf.spin_square()[0]:.6f}  2S+1 = {mf.spin_square()[1]:.6f}

Cohesive energy per atom: {cohesive_energy_per_atom:.6f} Hartree
                         = {cohesive_energy_per_atom*627.5:.2f} kcal/mol

HOMO-LUMO gap: {gap:.3f} eV

Mulliken charges per atom:
Pt1: {charges[0]:.4f}
Pt2: {charges[1]:.4f}
Pt3: {charges[2]:.4f}
Pt4: {charges[3]:.4f}
"""

    os.makedirs("results", exist_ok=True)

    with open("results/cluster_final.txt","w") as f:
        f.write(result_text)

    return mf, mol


def analyze_frontier_orbitals(mf, mol):
    """Analyze frontier molecular orbitals"""

    print("\n" + "-"*70)
    print("FRONTIER MOLECULAR ORBITALS ANALYSIS")
    print("-"*70)

    mo_coeff = mf.mo_coeff
    mo_energy = mf.mo_energy
    mo_occ = mf.mo_occ

    homo_idx = np.where(mo_occ > 0.5)[0][-1]

    orbital_energies = mo_energy * 27.2114

    print("Frontier orbital energies (eV):")

    for i in range(max(0, homo_idx-2), min(len(mo_energy), homo_idx+3)):
        occ = "occupied" if mo_occ[i] > 0.5 else "virtual"
        print(f"  Orbital {i+1}: {orbital_energies[i]:.3f} eV ({occ})")

    np.save('results/pt4_orbitals.npy', mo_coeff)
    np.save('results/pt4_energies.npy', mo_energy)
    np.save('results/pt4_occupancies.npy', mo_occ)

    print("\n✓ Orbital data saved for quantum computing interface")


if __name__ == "__main__":

    print("Platinum Tetramer Cluster Calculation")
    print("Model for catalytic nanoparticles")

    mf, mol = calculate_pt4_cluster()

    analyze_frontier_orbitals(mf, mol)

    print("\n" + "="*70)
    print("Pt₄ CLUSTER ANALYSIS COMPLETE")
    print("="*70)
