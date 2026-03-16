import streamlit as st
from style import load_css

# Page configuration - FULL SIZE
st.set_page_config(
    page_title="Pt Quantum Energy Dashboard",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_css()

# Custom CSS for FULL SIZE dashboard with proper text contrast
st.markdown("""
<style>
    /* Reset and full size */
    * {
        box-sizing: border-box;
    }
    
    .stApp {
        width: 100%;
        max-width: 100%;
        padding: 0;
        margin: 0;
    }
    
    .main > div {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    
    @media (min-width: 1920px) {
        .main > div {
            padding-left: 4rem;
            padding-right: 4rem;
        }
    }
    
    /* Global Styles - Full Width */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin: 1rem 0 3rem 0;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        width: 100%;
    }
    
    .main-header::before {
        content: "⚛";
        position: absolute;
        font-size: 20rem;
        opacity: 0.1;
        right: -50px;
        bottom: -80px;
        transform: rotate(15deg);
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        color: white;
    }
    
    .main-header p {
        font-size: 1.4rem;
        opacity: 0.95;
        max-width: 1000px;
        margin: 0 auto;
        color: white;
    }
    
    .section-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 4px solid #667eea;
        display: block;
        width: 100%;
        text-align: left;
    }
    
    /* Module Cards Grid - Full Width */
    .row-container {
        width: 100%;
        margin: 0;
        padding: 0;
    }
    
    .module-card {
        background: white;
        padding: 2rem 1.8rem;
        border-radius: 24px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        height: 100%;
        min-height: 380px;
        display: flex;
        flex-direction: column;
        border: 1px solid rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
        width: 100%;
    }
    
    .module-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .module-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .module-icon {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 8px 15px rgba(102, 126, 234, 0.3));
    }
    
    .module-title {
        font-size: 1.6rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        color: #1a1a1a;
    }
    
    .module-desc {
        font-size: 1rem;
        color: #4a4a4a;
        text-align: center;
        margin-bottom: 1.5rem;
        line-height: 1.6;
        flex-grow: 1;
        padding: 0 0.5rem;
        font-weight: 400;
    }
    
    .module-badge {
        display: inline-block;
        padding: 0.35rem 1.2rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 auto 1rem auto;
        text-align: center;
        width: fit-content;
    }
    
    .badge-classical {
        background: rgba(102, 126, 234, 0.1);
        color: #4a5568;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .badge-quantum {
        background: rgba(155, 89, 182, 0.1);
        color: #4a5568;
    }
    
    /* Feature tags container - FIXED CONTRAST */
    .features-container {
        margin: 1rem 0 1.5rem 0;
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        justify-content: center;
        padding: 0 0.5rem;
    }
    
    .feature-item {
        background: #e6e9f2;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #1a2639;
        border: 1px solid rgba(102, 126, 234, 0.3);
        display: inline-block;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .quantum-feature {
        background: #e8def0;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #2d1b3c;
        border: 1px solid rgba(155, 89, 182, 0.3);
        display: inline-block;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Module button - FIXED CONTRAST */
    .module-btn {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: #ffffff !important;
        text-align: center;
        padding: 1rem 1.5rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s;
        border: none;
        cursor: pointer;
        margin-top: auto;
        display: block;
        width: 100%;
        letter-spacing: 0.5px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .module-btn:hover {
        opacity: 0.9;
        transform: scale(1.02);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
        color: white !important;
    }
    
    .stats-panel {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecf5 100%);
        padding: 2.5rem;
        border-radius: 30px;
        margin: 3rem 0;
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 2rem;
        width: 100%;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .stat-item {
        text-align: center;
        flex: 1;
        min-width: 180px;
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        color: #2d3748;
        line-height: 1.2;
    }
    
    .stat-label {
        color: #4a5568;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .feature-tag {
        background: rgba(255,255,255,0.15);
        padding: 0.6rem 1.2rem;
        border-radius: 50px;
        font-size: 1rem;
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
        margin: 0 0.5rem;
        display: inline-block;
        font-weight: 500;
        backdrop-filter: blur(5px);
    }
    
    .footer {
        text-align: center;
        padding: 4rem 2rem 2rem;
        color: #4a5568;
        font-size: 1rem;
        border-top: 2px solid #e2e8f0;
        margin-top: 4rem;
        width: 100%;
    }
    
    .quantum-badge {
        background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%);
        color: white;
        padding: 0.35rem 1.2rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0 auto 1rem auto;
        width: fit-content;
        border: 1px solid rgba(255,255,255,0.2);
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Workflow container - Full Width */
    .workflow-wrapper {
        width: 100%;
        margin: 2rem 0;
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
    }
    
    .workflow-step {
        text-align: center;
        padding: 1.8rem 1rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        flex: 1;
        min-width: 160px;
        transition: transform 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .workflow-step:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.1);
        border-color: #667eea;
    }
    
    .workflow-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .workflow-text {
        font-size: 1rem;
        color: #2d3748;
        font-weight: 700;
        white-space: pre-line;
        line-height: 1.4;
    }
    
    .workflow-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        margin-top: 1.2rem;
        width: 50%;
        margin-left: auto;
        margin-right: auto;
        border-radius: 3px;
    }
    
    /* ===== NEW SPACING STYLES ADDED ===== */
    /* Add spacing between module rows */
    .stHorizontalBlock {
        gap: 2rem !important;
        margin-bottom: 2rem !important;
    }
    
    /* Add spacing after Classical Chemistry section */
    .classical-section-spacer {
        margin-bottom: 3rem;
        width: 100%;
    }
    
    /* Ensure quantum section has proper top margin */
    .quantum-section {
        margin-top: 4rem !important;
    }
    /* ===== END OF NEW SPACING STYLES ===== */
    
    /* Responsive adjustments */
    @media (max-width: 1200px) {
        .main-header h1 {
            font-size: 3rem;
        }
        
        .module-title {
            font-size: 1.4rem;
        }
    }
    
    @media (max-width: 768px) {
        .main > div {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .main-header {
            padding: 2.5rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2.2rem;
        }
        
        .main-header p {
            font-size: 1.1rem;
        }
        
        .section-header {
            font-size: 1.8rem;
        }
        
        .stats-panel {
            flex-direction: column;
            align-items: center;
            padding: 1.5rem;
        }
        
        .stat-item {
            width: 100%;
        }
        
        .workflow-wrapper {
            flex-direction: column;
            gap: 1rem;
        }
        
        .workflow-step {
            width: 100%;
        }
    }
    
    /* Ultra-wide screens */
    @media (min-width: 2000px) {
        .main-header h1 {
            font-size: 4rem;
        }
        
        .module-card {
            min-height: 420px;
        }
        
        .module-title {
            font-size: 1.8rem;
        }
        
        .module-desc {
            font-size: 1.1rem;
        }
    }
    
    /* Full width containers */
    .stColumn {
        width: 100%;
    }
    
    .row-widget {
        width: 100%;
    }
    
    .element-container {
        width: 100%;
    }
    
    /* Description text contrast fix */
    p, li, span {
        color: #2d3748;
    }
    
    /* Link styles */
    a {
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# Header - Full Width
st.markdown("""
<div class="main-header">
    <h1>⚛ Platinum Energy Level Estimation</h1>
    <p>Quantum Computing + Classical Chemistry Simulations for Platinum Systems</p>
    <div style="margin-top: 2.5rem; display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
        <span class="feature-tag">🧩 5 Classical Modules</span>
        <span class="feature-tag">💻 3 Quantum Modules</span>
        <span class="feature-tag">⚛ Platinum Catalysis</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Classical Chemistry Section
st.markdown('<div class="section-header">🔬 Classical Chemistry Simulations</div>', unsafe_allow_html=True)
st.markdown('<p style="color: #4a5568; margin-bottom: 2rem; font-size: 1.1rem; font-weight: 400;">First-principles calculations using PySCF with def2svp basis and ECP</p>', unsafe_allow_html=True)

classical_modules = [
    {
        "name": "Platinum Dimer",
        "icon": "⚛️",
        "desc": "Pt-Pt bond analysis, potential energy curves, singlet vs triplet states, and HOMO-LUMO gap calculation.",
        "page": "dimer",
        "color": "#667eea",
        "features": ["Bond optimization", "Spin states", "Orbital analysis"]
    },
    {
        "name": "Pt₄ Cluster",
        "icon": "💠",
        "desc": "Tetrahedral platinum cluster (Pt₄) for nanoparticle surface modeling and catalytic site analysis.",
        "page": "cluster",
        "color": "#4ECDC4",
        "features": ["DFT (PBE0)", "Cohesive energy", "Mulliken charges"]
    },
    {
        "name": "Pt Surface",
        "icon": "🌐",
        "desc": "10-atom surface model with 2 layers for catalysis studies and adsorption properties.",
        "page": "surface",
        "color": "#45B7D1",
        "features": ["Surface DOS", "Layer analysis", "Catalytic sites"]
    },
    {
        "name": "Pt₂ Interaction",
        "icon": "⚡",
        "desc": "Accurate interaction energy calculation: E_interaction = E(Pt₂) - 2E(Pt)",
        "page": "interaction",
        "color": "#96CEB4",
        "features": ["Binding energy", "Dissociation", "ECP treatment"]
    }
]

# Classical modules grid - Full width with reduced width (90%)
row1_col1, row1_col2 = st.columns(2, gap="large")
row2_col1, row2_col2 = st.columns(2, gap="large")

rows = [[row1_col1, row1_col2], [row2_col1, row2_col2]]

for row_idx, row in enumerate(rows):
    for col_idx, col in enumerate(row):
        module_idx = row_idx * 2 + col_idx
        if module_idx < len(classical_modules):
            module = classical_modules[module_idx]
            with col:
                features_html = "".join([f'<span class="feature-item">{f}</span>' for f in module["features"]])
                
                # ONLY CHANGE HERE: Added style="max-width: 90%; margin: 0 auto;" to reduce width
                st.markdown(f"""
                <div class="module-card" style="max-width: 90%; margin: 0 auto;">
                    <div class="module-icon">{module['icon']}</div>
                    <div class="module-badge badge-classical">⚛ Classical DFT/HF</div>
                    <div class="module-title">{module['name']}</div>
                    <div class="module-desc">{module['desc']}</div>
                    <div class="features-container">{features_html}</div>
                    <a href="/{module['page']}" target="_self" class="module-btn" style="background: {module['color']};">🚀 Launch Simulation →</a>
                </div>
                """, unsafe_allow_html=True)

# Spacer added here
st.markdown('<div class="classical-section-spacer"></div>', unsafe_allow_html=True)

# Quantum Computing Section - WITH NEW CLASS ADDED
st.markdown('<div class="section-header quantum-section">🧠 Quantum Computing Modules</div>', unsafe_allow_html=True)
st.markdown('<p style="color: #4a5568; margin-bottom: 2rem; font-size: 1.1rem; font-weight: 400;">Quantum algorithms for molecular simulation using Qiskit</p>', unsafe_allow_html=True)

quantum_modules = [
    {
        "name": "Molecule → Qubit",
        "icon": "🔀",
        "desc": "Transform molecular Hamiltonians to qubit operators using Jordan-Wigner mapping.",
        "page": "molecule_to_qubit",
        "color": "#9B59B6",
        "features": ["Fermionic op", "Pauli strings", "Qubit mapping"]
    },
    {
        "name": "VQE Solver",
        "icon": "🛠️",
        "desc": "Variational Quantum Eigensolver with COBYLA optimizer and TwoLocal ansatz.",
        "page": "vqe_solver",
        "color": "#3498DB",
        "features": ["Convergence", "Optimization", "Comparison"]
    },
    {
        "name": "Quantum VQE",
        "icon": "⚛️",
        "desc": "Advanced VQE with chemical bonding interpretation and eigenvalue analysis.",
        "page": "quantum_vqe",
        "color": "#E67E22",
        "features": ["Bond character", "Probabilities", "Energy gaps"]
    }
]

# Quantum modules grid - Full width (unchanged)
cols = st.columns(3, gap="large")
for col, module in zip(cols, quantum_modules):
    with col:
        features_html = "".join([f'<span class="quantum-feature">{f}</span>' for f in module["features"]])
        
        st.markdown(f"""
        <div class="module-card">
            <div class="module-icon">{module['icon']}</div>
            <div class="quantum-badge">⚛ Quantum Algorithm</div>
            <div class="module-title">{module['name']}</div>
            <div class="module-desc">{module['desc']}</div>
            <div class="features-container">{features_html}</div>
            <a href="/{module['page']}" target="_self" class="module-btn" style="background: {module['color']};">⚡ Run Simulation →</a>
        </div>
        """, unsafe_allow_html=True)

# System Information Panel - Full Width
st.markdown("""
<div class="stats-panel">
    <div class="stat-item">
        <div class="stat-number">def2svp</div>
        <div class="stat-label">Basis Set</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">PySCF</div>
        <div class="stat-label">Classical Engine</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">Qiskit</div>
        <div class="stat-label">Quantum Framework</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">Pt</div>
        <div class="stat-label">Platinum (Z=78)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Workflow Visualization - Full Width
st.markdown('<div class="section-header">🔄 Computational Workflow</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
workflow_steps = [
    ("🔬", "Classical\nCalculation", "PySCF"),
    ("🔀", "Qubit\nMapping", "Jordan-Wigner"),
    ("🛠️", "VQE\nOptimization", "COBYLA"),
    ("⚛️", "Energy\nExtraction", "Eigenvalues"),
    ("📊", "Analysis\n& Plotting", "Visualization")
]

for col, (icon, text, subtext) in zip([col1, col2, col3, col4, col5], workflow_steps):
    with col:
        st.markdown(f"""
        <div class="workflow-step">
            <div class="workflow-icon">{icon}</div>
            <div class="workflow-text">{text}</div>
            <div style="font-size: 0.85rem; color: #718096; margin-top: 0.3rem; font-weight: 500;">{subtext}</div>
            <div class="workflow-divider"></div>
        </div>
        """, unsafe_allow_html=True)

# Footer - Full Width
st.markdown("""
<div class="footer">
    <p style="font-size: 1.2rem; margin-bottom: 1.5rem; font-weight: 600; color: #2d3748;">⚛ Platinum Energy Level Estimation using Quantum Computing</p>
    <p style="font-size: 1rem; opacity: 0.8; margin-bottom: 2rem; color: #4a5568;">
        Built with Streamlit • PySCF • Qiskit • def2svp • ECP
    </p>
    <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 1rem;">
        <span style="color: #4a5568; font-weight: 500;">🔬 4 Classical Modules</span>
        <span style="color: #4a5568; font-weight: 500;">🧠 3 Quantum Modules</span>
        <span style="color: #4a5568; font-weight: 500;">⚛ Platinum Catalysis</span>
    </div>
    <p style="font-size: 0.9rem; margin-top: 2rem; opacity: 0.6; color: #718096;">
        Version 3.0 | Designed for Quantum Chemistry Research
    </p>
</div>
""", unsafe_allow_html=True)
