import streamlit as st
import subprocess
import os
from style import load_css

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Molecule → Qubit Hamiltonian",
    page_icon="🔀",
    layout="wide"
)

# Load custom CSS
load_css()

# Custom CSS for this page
st.markdown("""
<style>
    .back-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        background: white;
        color: #9B59B6;
        padding: 10px 20px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        z-index: 999;
        box-shadow: 0 4px 15px rgba(155, 89, 182, 0.2);
        transition: all 0.3s;
        border: 1px solid rgba(155, 89, 182, 0.2);
        backdrop-filter: blur(10px);
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
        border: none;
        cursor: pointer;
    }
    
    .back-btn:hover {
        transform: translateX(-5px);
        box-shadow: 0 6px 20px rgba(155, 89, 182, 0.3);
        background: linear-gradient(90deg, #9B59B6 0%, #8E44AD 100%);
        color: white;
    }
    
    .back-btn::before {
        content: "←";
        font-size: 1.2rem;
        font-weight: bold;
        margin-right: 5px;
    }
    
    .header-container {
        text-align: center;
        margin: 2rem 0 3rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(155, 89, 182, 0.3);
    }
    
    .header-container h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .header-container p {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    .run-button-container {
        text-align: center;
        margin: 2rem 0;
    }
    
    .run-button {
        background: linear-gradient(90deg, #9B59B6 0%, #8E44AD 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.3rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(155, 89, 182, 0.3);
    }
    
    .run-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(155, 89, 182, 0.4);
    }
    
    .info-panel {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #9B59B6;
    }
    
    .feature-tag {
        display: inline-block;
        background: #f0e6f5;
        color: #9B59B6;
        padding: 0.3rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        margin: 0.2rem;
        font-weight: 500;
    }
    
    .result-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid #eef2f6;
    }
    
    .stCode {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    
    .success-message {
        background: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    
    .info-message {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
    
    .error-message {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #dc3545;
        color: #721c24;
    }
    
    .mapping-diagram {
        background: linear-gradient(135deg, #667eea 0%, #9B59B6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
        text-align: center;
    }
    
    .mapping-arrow {
        font-size: 2rem;
        margin: 0 1rem;
    }
    
    .hamiltonian-preview {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
    }
    
    .step-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        height: 100%;
    }
    
    .step-number {
        background: #9B59B6;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem auto;
        font-weight: bold;
    }
    
    /* New class for button spacing */
    .button-spacer {
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("⬅ Back to Dashboard", key="back_btn"):
    st.switch_page("app.py")

# Header
st.markdown("""
<div class="header-container">
    <h1>🔀 Molecule → Qubit Hamiltonian</h1>
    <p>Transform Molecular Hamiltonians to Qubit Operators</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for tracking if simulation was run
if 'molecule_qubit_run' not in st.session_state:
    st.session_state.molecule_qubit_run = False

# Main content layout
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # Info panel
    st.markdown("""
    <div class="info-panel">
        <h3 style="color: #333; margin-bottom: 1rem;">🔁 Quantum Mapping Details</h3>
        <p style="color: #666;">This module converts a molecular Hamiltonian to qubit representation using:</p>
        <div style="margin: 1rem 0;">
            <span class="feature-tag">⚛ H₂ molecule</span>
            <span class="feature-tag">📊 STO-3G basis</span>
            <span class="feature-tag">🔄 Jordan-Wigner mapping</span>
            <span class="feature-tag">🧮 PySCF driver</span>
            <span class="feature-tag">🔢 Pauli strings</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mapping visualization
    st.markdown("""
    <div class="mapping-diagram">
        <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">
            <span style="font-size: 1.5rem;">H₂ Molecule</span>
            <span class="mapping-arrow">→</span>
            <span style="font-size: 1.5rem;">Fermionic Operator</span>
            <span class="mapping-arrow">→</span>
            <span style="font-size: 1.5rem;">Qubit Hamiltonian</span>
        </div>
        <p style="margin-top: 1rem; opacity: 0.9;">Jordan-Wigner Transformation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Molecule info
    st.markdown("""
    <div style="background: #f0e6f5; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: #333; margin-bottom: 0.5rem;"><strong>📌 Test System:</strong></p>
        <p style="color: #666; margin: 0;">H₂ molecule • Bond length: 0.74 Å • STO-3G basis • 2 electrons</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add spacer div
    st.markdown('<div class="button-spacer"></div>', unsafe_allow_html=True)
    
    # Run button
    run = st.button("🚀 RUN MOLECULE TO QUBIT CONVERSION", key="run_btn", use_container_width=True)

# Handle simulation run
if run:
    st.session_state.molecule_qubit_run = True
    
    with st.container():
        st.markdown('<div class="info-message">⚙ Running quantum mapping... Generating qubit Hamiltonian.</div>', unsafe_allow_html=True)
        
        with st.spinner("Converting molecule to qubit representation..."):
            # Run the molecule to qubit script
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "molecule_to_qubit.py")
            result = subprocess.run(["python3", script_path], 
                                   capture_output=True, 
                                   text=True)
            
            if result.returncode == 0:
                st.markdown('<div class="success-message">✅ Conversion completed successfully!</div>', unsafe_allow_html=True)
                
                # Show output in expander
                with st.expander("View calculation output"):
                    st.code(result.stdout, language="bash")
            else:
                st.markdown('<div class="error-message">❌ Conversion failed. Check the error message below.</div>', unsafe_allow_html=True)
                st.code(result.stderr, language="bash")
                st.session_state.molecule_qubit_run = False

# Results section - ONLY show if simulation has been run
if st.session_state.molecule_qubit_run:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>📊 Conversion Results</h2>", unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # Check for result file
        result_file = "results/molecule_qubit_final.txt"
        
        # Display results
        if os.path.exists(result_file):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #9B59B6; margin-bottom: 1rem;">📝 Qubit Hamiltonian</h3>
            """, unsafe_allow_html=True)
            
            with open(result_file, 'r') as f:
                content = f.read()
            
            # Format the Hamiltonian nicely
            st.markdown('<div class="hamiltonian-preview">', unsafe_allow_html=True)
            st.code(content, language="text")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add explanation
            st.markdown("""
            <div style="background: #f0e6f5; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <p style="color: #333; margin: 0;"><strong>📌 Interpretation:</strong></p>
                <p style="color: #666; margin-top: 0.5rem;">
                • Each term is a Pauli string (I, X, Y, Z operators)<br>
                • Coefficients represent interaction strengths<br>
                • This Hamiltonian can now be executed on quantum hardware
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠ Result file not found. There might be an issue with the conversion.</div>', unsafe_allow_html=True)

# Additional information section (always visible)
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>ℹ About the Mapping Process</h2>", unsafe_allow_html=True)

# Mapping steps
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div>
        <h4 style="color: #9B59B6;">Molecular Hamiltonian</h4>
        <p style="color: #666;">H = Σ h<sub>pq</sub> a<sub>p</sub>† a<sub>q</sub> + Σ g<sub>pqrs</sub> a<sub>p</sub>† a<sub>q</sub>† a<sub>r</sub> a<sub>s</sub></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div>
        <h4 style="color: #9B59B6;">Fermionic Operators</h4>
        <p style="color: #666;">Creation/annihilation operators acting on fermionic modes</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div>
        <h4 style="color: #9B59B6;">Jordan-Wigner Mapping</h4>
        <p style="color: #666;">a<sub>p</sub>† → (∏ σ<sub>k</sub>z) σ<sub>p</sub>+</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">4</div>
        <h4 style="color: #9B59B6;">Qubit Hamiltonian</h4>
        <p style="color: #666;">H = Σ c<sub>i</sub> P<sub>i</sub> (Pauli strings)</p>
    </div>
    """, unsafe_allow_html=True)

# Detailed explanation
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #333; margin: 2rem 0;'>🔬 Jordan-Wigner Transformation</h3>", unsafe_allow_html=True)

exp_col1, exp_col2 = st.columns(2)

with exp_col1:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
        <h4 style="color: #9B59B6;">Fermion → Qubit Mapping</h4>
        <p style="color: #666; font-family: monospace; background: #f5f5f5; padding: 1rem; border-radius: 5px;">
        a<sub>j</sub>† = 1/2 (X<sub>j</sub> - iY<sub>j</sub>) ⊗ Z<sub>j-1</sub> ⊗ ... ⊗ Z<sub>0</sub><br>
        a<sub>j</sub> = 1/2 (X<sub>j</sub> + iY<sub>j</sub>) ⊗ Z<sub>j-1</sub> ⊗ ... ⊗ Z<sub>0</sub>
        </p>
    </div>
    """, unsafe_allow_html=True)

with exp_col2:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
        <h4 style="color: #9B59B6;">Pauli Operators</h4>
        <p style="color: #666;">
        • X = |0⟩⟨1| + |1⟩⟨0|<br>
        • Y = -i|0⟩⟨1| + i|1⟩⟨0|<br>
        • Z = |0⟩⟨0| - |1⟩⟨1|<br>
        • I = |0⟩⟨0| + |1⟩⟨1|
        </p>
    </div>
    """, unsafe_allow_html=True)

# Next steps
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #333; margin: 2rem 0;'>➡ Next Steps</h3>", unsafe_allow_html=True)

next_col1, next_col2, next_col3 = st.columns(3)

with next_col1:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #9B59B6;">VQE Solver</h4>
        <p style="color: #666;">Run VQE on the qubit Hamiltonian</p>
        <a href="/vqe_solver" target="_self" style="text-decoration: none; color: #9B59B6;">→ Go to VQE</a>
    </div>
    """, unsafe_allow_html=True)

with next_col2:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #9B59B6;">Quantum VQE</h4>
        <p style="color: #666;">Advanced VQE with chemical interpretation</p>
        <a href="/quantum_vqe" target="_self" style="text-decoration: none; color: #9B59B6;">→ Go to Quantum VQE</a>
    </div>
    """, unsafe_allow_html=True)

with next_col3:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #9B59B6;">Classical Methods</h4>
        <p style="color: #666;">Compare with classical Pt calculations</p>
        <a href="/dimer" target="_self" style="text-decoration: none; color: #9B59B6;">→ Go to Dimer</a>
    </div>
    """, unsafe_allow_html=True)

# Navigation footer (always visible)
st.markdown("---")
col_next1, col_next2, col_next3 = st.columns(3)
with col_next1:
    st.page_link("pages/vqe_solver.py", label="→ Next: VQE Solver", use_container_width=True)
with col_next2:
    st.page_link("pages/quantum_vqe.py", label="→ Next: Quantum VQE", use_container_width=True)
with col_next3:
    st.page_link("pages/dimer.py", label="← Back to Classical", use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #999; font-size: 0.9rem;">
    <p>🔀 Molecule → Qubit Hamiltonian | Part of the Platinum Energy Level Estimation Project</p>
</div>
""", unsafe_allow_html=True)
