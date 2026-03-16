import streamlit as st
import subprocess
import os
from PIL import Image
from style import load_css

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Quantum VQE Simulation",
    page_icon="⚛",
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
        color: #E67E22;
        padding: 10px 20px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        z-index: 999;
        box-shadow: 0 4px 15px rgba(230, 126, 34, 0.2);
        transition: all 0.3s;
        border: 1px solid rgba(230, 126, 34, 0.2);
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
        box-shadow: 0 6px 20px rgba(230, 126, 34, 0.3);
        background: linear-gradient(90deg, #E67E22 0%, #D35400 100%);
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
        background: linear-gradient(135deg, #E67E22 0%, #D35400 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(230, 126, 34, 0.3);
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
        background: linear-gradient(90deg, #E67E22 0%, #D35400 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.3rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(230, 126, 34, 0.3);
    }
    
    .run-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(230, 126, 34, 0.4);
    }
    
    .info-panel {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #E67E22;
    }
    
    .feature-tag {
        display: inline-block;
        background: #fef0e5;
        color: #E67E22;
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
    
    .bond-analysis {
        background: linear-gradient(135deg, #667eea 0%, #E67E22 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
        text-align: center;
    }
    
    .state-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .state-prob {
        font-size: 1.5rem;
        font-weight: bold;
        color: #E67E22;
    }
    
    .bond-character {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
        padding: 1rem;
        background: #fef0e5;
        border-radius: 10px;
    }
    
    .character-box {
        text-align: center;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        background: white;
    }
    
    .eigenvalue-table {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
    }
    
    /* Bond analysis card styles */
    .bond-card {
        text-align: center;
        padding: 1.5rem 1rem;
        background: #f8f9fa;
        border-radius: 15px;
        height: 100%;
        border: 1px solid #eef2f6;
        transition: transform 0.3s ease;
    }
    
    .bond-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .bond-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .bond-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .bond-percentage {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
    }
    
    .bond-bar-bg {
        background: #e9ecef;
        height: 12px;
        border-radius: 6px;
        margin: 0.8rem 0;
        overflow: hidden;
    }
    
    .bond-bar-fill {
        height: 12px;
        border-radius: 6px;
        transition: width 0.5s ease;
    }
    
    .bond-description {
        color: #666;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    .legend-box {
        display: flex;
        align-items: center;
        margin-right: 1.5rem;
    }
    
    .legend-color {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("⬅ Back to Dashboard", key="back_btn"):
    st.switch_page("app.py")

# Header
st.markdown("""
<div class="header-container">
    <h1>⚛ Quantum VQE Simulation</h1>
    <p>Advanced VQE with Chemical Bonding Interpretation</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for tracking if simulation was run
if 'quantum_vqe_run' not in st.session_state:
    st.session_state.quantum_vqe_run = False

# Main content layout
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # Info panel
    st.markdown("""
    <div class="info-panel">
        <h3 style="color: #333; margin-bottom: 1rem;">⚛ Quantum VQE Details</h3>
        <p style="color: #666;">This module runs an advanced VQE simulation with chemical interpretation:</p>
        <div style="margin: 1rem 0;">
            <span class="feature-tag">🧮 2-qubit system</span>
            <span class="feature-tag">🔄 Heisenberg model</span>
            <span class="feature-tag">📊 J = -0.15, h = 0.08</span>
            <span class="feature-tag">🎯 CNOT + Ry ansatz</span>
            <span class="feature-tag">🔬 Chemical bonding</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hamiltonian display
    st.markdown("""
    <div style="background: #fef0e5; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: #333; margin-bottom: 0.5rem;"><strong>📌 Hamiltonian:</strong></p>
        <p style="color: #666; font-family: monospace; background: white; padding: 1rem; border-radius: 5px;">
        H = c·II + h·(ZI + IZ) + J·(XX + YY + ZZ)<br>
        J = -0.15 (exchange coupling)<br>
        h = 0.08 (local field)<br>
        c = -1.0 (constant)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bond interpretation preview
    st.markdown("""
    <div class="bond-analysis">
        <h3 style="color: white; margin-bottom: 1rem;">🔬 Chemical Bond Interpretation</h3>
        <p style="opacity: 0.9;">The quantum state is mapped to chemical bonding concepts:</p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
            <div><strong>|00⟩</strong> → No bond</div>
            <div><strong>|01⟩, |10⟩</strong> → Ionic character</div>
            <div><strong>|11⟩</strong> → Covalent bond</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Run button
    run = st.button("🚀 RUN QUANTUM VQE", key="run_btn", use_container_width=True)

# Handle simulation run
if run:
    st.session_state.quantum_vqe_run = True
    
    with st.container():
        st.markdown('<div class="info-message">⚙ Running Quantum VQE simulation... This may take a few moments.</div>', unsafe_allow_html=True)
        
        with st.spinner("Optimizing quantum circuit and analyzing chemical bonding..."):
            # Run the quantum VQE script
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vqe_2.py")
            result = subprocess.run(["python3", script_path], 
                                   capture_output=True, 
                                   text=True)
            
            if result.returncode == 0:
                st.markdown('<div class="success-message">✅ Quantum VQE completed successfully!</div>', unsafe_allow_html=True)
                
                # Show output in expander
                with st.expander("View calculation output"):
                    st.code(result.stdout, language="bash")
            else:
                st.markdown('<div class="error-message">❌ Quantum VQE failed. Check the error message below.</div>', unsafe_allow_html=True)
                st.code(result.stderr, language="bash")
                st.session_state.quantum_vqe_run = False

# Results section - ONLY show if simulation has been run
if st.session_state.quantum_vqe_run:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>📊 Quantum VQE Results</h2>", unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # Check for result files
        result_file = "results/quantum_vqe_final.txt"
        results_img = "results/vqe_results_fixed.png"
        
        # Display text results
        if os.path.exists(result_file):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #E67E22; margin-bottom: 1rem;">📝 Final Results</h3>
            """, unsafe_allow_html=True)
            
            with open(result_file, 'r') as f:
                content = f.read()
            
            # Parse and display key results
            import re
            
            # Extract VQE energy
            vqe_match = re.search(r'VQE energy: (.*)', content)
            exact_match = re.search(r'Exact energy: (.*)', content)
            error_match = re.search(r'Error: (.*)', content)
            theta_match = re.search(r'Optimal parameter θ: (.*)', content)
            
            if vqe_match and exact_match:
                vqe_energy = vqe_match.group(1)
                exact_energy = exact_match.group(1)
                error = error_match.group(1) if error_match else "N/A"
                theta = theta_match.group(1) if theta_match else "N/A"
                
                # Energy comparison
                st.markdown(f"""
                <div style="display: flex; justify-content: space-around; margin: 1rem 0;">
                    <div style="text-align: center; padding: 1rem; background: #fef0e5; border-radius: 10px; flex: 1; margin: 0 0.5rem;">
                        <div style="color: #666; font-size: 0.9rem;">VQE Energy</div>
                        <div style="color: #E67E22; font-size: 1.8rem; font-weight: bold;">{vqe_energy}</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #fef0e5; border-radius: 10px; flex: 1; margin: 0 0.5rem;">
                        <div style="color: #666; font-size: 0.9rem;">Exact Energy</div>
                        <div style="color: #D35400; font-size: 1.8rem; font-weight: bold;">{exact_energy}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Optimal parameter
                st.markdown(f"""
                <div style="text-align: center; margin: 1rem 0;">
                    <span style="background: #E67E22; color: white; padding: 0.5rem 1rem; border-radius: 50px;">
                        Optimal θ = {theta} rad
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            # Extract bonding analysis
            covalent_match = re.search(r'Covalent character: (.*)', content)
            ionic_match = re.search(r'Ionic character: (.*)', content)
            nobond_match = re.search(r'No bond: (.*)', content)
            
            if covalent_match and ionic_match and nobond_match:
                covalent = float(covalent_match.group(1))
                ionic = float(ionic_match.group(1))
                nobond = float(nobond_match.group(1))
                
                st.markdown("""
                <h4 style="color: #333; margin: 2rem 0 1.5rem 0; text-align: center; font-size: 1.5rem;">🔬 Chemical Bond Analysis</h4>
                """, unsafe_allow_html=True)
                
                # Simple legend
                st.markdown(f"""
                <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 2rem; flex-wrap: wrap; background: white; padding: 1rem; border-radius: 50px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 20px; height: 20px; background: #E67E22; border-radius: 4px; margin-right: 8px;"></div>
                        <span style="font-weight: 500;">Covalent: <strong style="color: #E67E22;">{covalent*100:.1f}%</strong></span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 20px; height: 20px; background: #3498DB; border-radius: 4px; margin-right: 8px;"></div>
                        <span style="font-weight: 500;">Ionic: <strong style="color: #3498DB;">{ionic*100:.1f}%</strong></span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 20px; height: 20px; background: #95a5a6; border-radius: 4px; margin-right: 8px;"></div>
                        <span style="font-weight: 500;">No Bond: <strong style="color: #95a5a6;">{nobond*100:.1f}%</strong></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Create three columns for the bond cards
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="bond-card">
                        <div class="bond-icon" style="color: #E67E22;">⚛</div>
                        <div class="bond-title" style="color: #E67E22;">Covalent Bond</div>
                        <div class="bond-percentage" style="color: #E67E22;">{covalent*100:.1f}%</div>
                        <div class="bond-bar-bg">
                            <div class="bond-bar-fill" style="background: #E67E22; width: {covalent*100}%;"></div>
                        </div>
                        <div class="bond-description">|11⟩ - Shared electron pair</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="bond-card">
                        <div class="bond-icon" style="color: #3498DB;">⚡</div>
                        <div class="bond-title" style="color: #3498DB;">Ionic Character</div>
                        <div class="bond-percentage" style="color: #3498DB;">{ionic*100:.1f}%</div>
                        <div class="bond-bar-bg">
                            <div class="bond-bar-fill" style="background: #3498DB; width: {ionic*100}%;"></div>
                        </div>
                        <div class="bond-description">|01⟩+|10⟩ - Electron on one atom</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="bond-card">
                        <div class="bond-icon" style="color: #95a5a6;">○</div>
                        <div class="bond-title" style="color: #95a5a6;">No Bond</div>
                        <div class="bond-percentage" style="color: #95a5a6;">{nobond*100:.1f}%</div>
                        <div class="bond-bar-bg">
                            <div class="bond-bar-fill" style="background: #95a5a6; width: {nobond*100}%;"></div>
                        </div>
                        <div class="bond-description">|00⟩ - No electron sharing</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Extract eigenvalues
            eigenvalues = re.findall(r'E\d.*: (.*)', content)
            if eigenvalues:
                st.markdown("""
                <h4 style="color: #333; margin: 2rem 0 1rem 0;">📊 Eigenvalue Spectrum</h4>
                """, unsafe_allow_html=True)
                
                eigen_html = "<div class='eigenvalue-table'>"
                for i, val in enumerate(eigenvalues[:4]):
                    color = "#e74c3c" if i == 0 else "#3498db"
                    eigen_html += f'<div style="color: {color};">E{i}: {val}</div>'
                eigen_html += "</div>"
                st.markdown(eigen_html, unsafe_allow_html=True)
            
            st.code(content, language="text")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠ Result file not found. There might be an issue with the calculation.</div>', unsafe_allow_html=True)
        
        # Display results plot
        if os.path.exists(results_img):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #E67E22; margin-bottom: 1rem;">📈 VQE Analysis Dashboard</h3>
            """, unsafe_allow_html=True)
            
            image = Image.open(results_img)
            st.image(image, use_container_width=True)
            
            # Add interpretation
            st.markdown("""
            <div style="background: #fef0e5; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <p style="color: #333; margin: 0;"><strong>📌 Multi-panel Analysis:</strong></p>
                <ul style="color: #666; margin-top: 0.5rem;">
                    <li><strong>Top left:</strong> VQE energy convergence</li>
                    <li><strong>Top middle:</strong> Parameter optimization</li>
                    <li><strong>Top right:</strong> Energy landscape</li>
                    <li><strong>Bottom left:</strong> Final quantum state probabilities</li>
                    <li><strong>Bottom middle:</strong> Eigenvalue spectrum</li>
                    <li><strong>Bottom right:</strong> Results summary</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠ Results plot not found. There might be an issue with the calculation.</div>', unsafe_allow_html=True)

# Additional information section (always visible)
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>ℹ About Quantum VQE</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #E67E22;">🎯 Features</h3>
        <p style="color: #666;">• Custom Heisenberg Hamiltonian</p>
        <p style="color: #666;">• Chemical bonding interpretation</p>
        <p style="color: #666;">• Full eigenvalue spectrum</p>
        <p style="color: #666;">• State probability analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #E67E22;">⚙ Circuit</h3>
        <p style="color: #666; font-family: monospace;">|ψ(θ)⟩ = CNOT · (Ry(θ) ⊗ I) · |00⟩</p>
        <p style="color: #666;">Single parameter ansatz</p>
        <p style="color: #666;">Captures entanglement</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #E67E22;">📊 Output</h3>
        <p style="color: #666;">• Ground state energy</p>
        <p style="color: #666;">• Bond character analysis</p>
        <p style="color: #666;">• Complete eigenvalue spectrum</p>
        <p style="color: #666;">• Comprehensive plots</p>
    </div>
    """, unsafe_allow_html=True)

# Quantum State Interpretation
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #333; margin: 2rem 0;'>🔬 Quantum State → Chemical Bonding</h3>", unsafe_allow_html=True)

state_col1, state_col2, state_col3, state_col4 = st.columns(4)

with state_col1:
    st.markdown("""
    <div class="state-card">
        <div style="font-size: 2rem; color: #95a5a6;">|00⟩</div>
        <div class="state-prob">No Bond</div>
        <div style="color: #666; font-size: 0.9rem;">Both sites unoccupied</div>
    </div>
    """, unsafe_allow_html=True)

with state_col2:
    st.markdown("""
    <div class="state-card">
        <div style="font-size: 2rem; color: #3498DB;">|01⟩</div>
        <div class="state-prob">Ionic</div>
        <div style="color: #666; font-size: 0.9rem;">Electron on site 2</div>
    </div>
    """, unsafe_allow_html=True)

with state_col3:
    st.markdown("""
    <div class="state-card">
        <div style="font-size: 2rem; color: #3498DB;">|10⟩</div>
        <div class="state-prob">Ionic</div>
        <div style="color: #666; font-size: 0.9rem;">Electron on site 1</div>
    </div>
    """, unsafe_allow_html=True)

with state_col4:
    st.markdown("""
    <div class="state-card">
        <div style="font-size: 2rem; color: #E67E22;">|11⟩</div>
        <div class="state-prob">Covalent</div>
        <div style="color: #666; font-size: 0.9rem;">Shared electron pair</div>
    </div>
    """, unsafe_allow_html=True)

# Navigation footer (always visible)
st.markdown("---")
col_next1, col_next2, col_next3 = st.columns(3)
with col_next1:
    st.page_link("pages/molecule_to_qubit.py", label="← Previous: Molecule → Qubit", use_container_width=True)
with col_next2:
    st.page_link("pages/vqe_solver.py", label="← Previous: VQE Solver", use_container_width=True)
with col_next3:
    st.page_link("pages/dimer.py", label="← Back to Classical", use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #999; font-size: 0.9rem;">
    <p>⚛ Quantum VQE Simulation | Part of the Platinum Energy Level Estimation Project</p>
</div>
""", unsafe_allow_html=True)
