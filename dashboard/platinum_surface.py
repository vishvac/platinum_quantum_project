#!/usr/bin/env python3
"""
PLATINUM SURFACE MODEL (10 atoms)
Simplified model for catalytic surfaces
"""

import numpy as np
from pyscf import gto, scf, dft
import matplotlib.pyplot as plt
import os


def create_pt_surface_model():
    """Create small Pt surface model (2-layer slab)"""

    print("\n" + "="*70)
    print("PLATINUM SURFACE MODEL (10 atoms)")
    print("="*70)

    # Create a small surface model (2x2 surface with 2 layers)

    layer1 = [
        [0.0, 0.0, 0.0],
        [2.77, 0.0, 0.0],
        [0.0, 2.77, 0.0],
        [2.77, 2.77, 0.0]
    ]

    layer2 = [
        [1.385, 1.385, 2.24],
        [4.155, 1.385, 2.24],
        [1.385, 4.155, 2.24],
        [4.155, 4.155, 2.24]
    ]

    extra = [
        [1.385, -1.385, -2.24],
        [4.155, -1.385, -2.24]
    ]

    coords = layer1 + layer2 + extra

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

    # -------- Visualization --------

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['blue', 'green', 'red']

    for i, coord in enumerate(coords):
        layer_idx = 0 if i < 4 else (1 if i < 8 else 2)

        ax.scatter(coord[0], coord[1], coord[2],
                   s=300,
                   c=colors[layer_idx],
                   label=f'Layer {layer_idx+1}' if i in [0,4,8] else "")

    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlabel('Z (Å)')
    ax.set_title('Pt₁₀ Surface Model')
    ax.legend()

    os.makedirs("results", exist_ok=True)

    plt.savefig('results/pt_surface_model.png', dpi=300, bbox_inches='tight')
    plt.show()

    return mol


def analyze_surface_properties():
    """Calculate surface properties"""

    mol = create_pt_surface_model()

    print("\nSurface model details:")
    print(f"  Number of atoms: {len(mol.atom)}")
    print(f"  Number of electrons: {mol.nelectron}")
    print(f"  Basis functions: {mol.nao}")

    print("\nRunning DFT calculation (PBE functional)...")

    mf = dft.RKS(mol)
    mf.xc = 'pbe'
    mf.conv_tol = 1e-6
    mf.max_cycle = 150

    energy = mf.kernel()

    print(f"\nTotal energy: {energy:.6f} Hartree")
    print(f"Energy per atom: {energy/len(mol.atom):.6f} Hartree")

    # -------- SAVE FINAL RESULT FOR DASHBOARD --------

    result_text = f"""
SCF energy = {mf.e_tot}

Total energy: {energy:.6f} Hartree
Energy per atom: {energy/len(mol.atom):.6f} Hartree
"""

    os.makedirs("results", exist_ok=True)

    with open("results/surface_final.txt", "w") as f:
        f.write(result_text)

    # -------- Density of States --------

    print("\nCalculating approximate Density of States...")

    mo_energy = mf.mo_energy
    mo_occ = mf.mo_occ

    plt.figure(figsize=(10, 6))

    energies = np.linspace(min(mo_energy)-1, max(mo_energy)+1, 1000)
    dos = np.zeros_like(energies)

    for e in mo_energy:
        dos += np.exp(-(energies - e)**2 / 0.01)

    plt.plot(energies*27.2114, dos, 'b-', linewidth=2)

    plt.axvline(
        x=mo_energy[mo_occ > 0.5][-1]*27.2114,
        color='r',
        linestyle='--',
        label='Fermi Level'
    )

    plt.xlabel('Energy (eV)')
    plt.ylabel('Density of States (arb. units)')
    plt.title('Approximate Density of States - Pt Surface Model')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.savefig('results/pt_surface_dos.png', dpi=300, bbox_inches='tight')
    plt.show()

    return mf, mol


if __name__ == "__main__":

    print("Platinum Surface Model for Catalysis")

    mf, mol = analyze_surface_properties()

    print("\n" + "="*70)
    print("SURFACE MODEL ANALYSIS COMPLETE")
    print("="*70)

    print("\nThis model provides insights into:")
    print("- Surface electronic structure")
    print("- Catalytic active sites")
    print("- Adsorption properties")

    print("\nNext: Use this for adsorption studies (H₂, CO, O₂ on Pt)")
