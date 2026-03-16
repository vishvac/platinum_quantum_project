import streamlit as st
import subprocess
import os
from PIL import Image
from style import load_css

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="VQE Quantum Solver",
    page_icon="🛠️",
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
        color: #3498DB;
        padding: 10px 20px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        z-index: 999;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.2);
        transition: all 0.3s;
        border: 1px solid rgba(52, 152, 219, 0.2);
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
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.3);
        background: linear-gradient(90deg, #3498DB 0%, #2980B9 100%);
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
        background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(52, 152, 219, 0.3);
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
        background: linear-gradient(90deg, #3498DB 0%, #2980B9 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.3rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
    }
    
    .run-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4);
    }
    
    .info-panel {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #3498DB;
    }
    
    .feature-tag {
        display: inline-block;
        background: #e1f0fa;
        color: #3498DB;
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
    
    .vqe-diagram {
        background: linear-gradient(135deg, #3498DB 0%, #9B59B6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
        text-align: center;
    }
    
    .vqe-arrow {
        font-size: 2rem;
        margin: 0 1rem;
    }
    
    .energy-comparison {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    .energy-box {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        background: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .energy-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3498DB;
    }
    
    .energy-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    .error-badge {
        background: #e74c3c;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("⬅ Back to Dashboard", key="back_btn"):
    st.switch_page("app.py")

# Header
st.markdown("""
<div class="header-container">
    <h1>🛠️  VQE Quantum Solver</h1>
    <p>Variational Quantum Eigensolver for Molecular Energy</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for tracking if simulation was run
if 'vqe_solver_run' not in st.session_state:
    st.session_state.vqe_solver_run = False

# Main content layout
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # Info panel
    st.markdown("""
    <div class="info-panel">
        <h3 style="color: #333; margin-bottom: 1rem;">🛠️  VQE Algorithm Details</h3>
        <p style="color: #666;">This module runs a VQE calculation on H₂ molecule using:</p>
        <div style="margin: 1rem 0;">
            <span class="feature-tag">⚛ H₂ molecule</span>
            <span class="feature-tag">📊 STO-3G basis</span>
            <span class="feature-tag">🔄 TwoLocal ansatz</span>
            <span class="feature-tag">📈 COBYLA optimizer</span>
            <span class="feature-tag">🎯 100 iterations</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # VQE Diagram
    st.markdown("""
    <div class="vqe-diagram">
        <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">
            <span style="font-size: 1.5rem;">Initial State</span>
            <span class="vqe-arrow">→</span>
            <span style="font-size: 1.5rem;">Parameterized Circuit</span>
            <span class="vqe-arrow">→</span>
            <span style="font-size: 1.5rem;">Measure Energy</span>
            <span class="vqe-arrow">↺</span>
        </div>
        <p style="margin-top: 1rem; opacity: 0.9;">Classical Optimization Loop</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Algorithm steps
    st.markdown("""
    <div style="background: #f0f7fc; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: #333; margin-bottom: 0.5rem;"><strong>📌 VQE Workflow:</strong></p>
        <ol style="color: #666; margin-left: 1rem;">
            <li>Prepare qubit Hamiltonian from molecule</li>
            <li>Create parameterized quantum circuit (ansatz)</li>
            <li>Measure expectation value</li>
            <li>Optimize parameters classically</li>
            <li>Converge to ground state energy</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Run button
    run = st.button("🚀 RUN VQE SOLVER", key="run_btn", use_container_width=True)

# Handle simulation run
if run:
    st.session_state.vqe_solver_run = True
    
    with st.container():
        st.markdown('<div class="info-message">⚙ Running VQE calculation... This may take a few moments.</div>', unsafe_allow_html=True)
        
        with st.spinner("Optimizing quantum circuit parameters..."):
            # Run the VQE solver script
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vqe_solver.py")
            result = subprocess.run(["python3", script_path], 
                                   capture_output=True, 
                                   text=True)
            
            if result.returncode == 0:
                st.markdown('<div class="success-message">✅ VQE calculation completed successfully!</div>', unsafe_allow_html=True)
                
                # Show output in expander
                with st.expander("View calculation output"):
                    st.code(result.stdout, language="bash")
            else:
                st.markdown('<div class="error-message">❌ VQE calculation failed. Check the error message below.</div>', unsafe_allow_html=True)
                st.code(result.stderr, language="bash")
                st.session_state.vqe_solver_run = False

# Results section - ONLY show if simulation has been run
if st.session_state.vqe_solver_run:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>📊 VQE Results</h2>", unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # Check for result files
        result_file = "results/vqe_final.txt"
        convergence_img = "results/vqe_convergence.png"
        
        # Display text results
        if os.path.exists(result_file):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #3498DB; margin-bottom: 1rem;">📝 Final Results</h3>
            """, unsafe_allow_html=True)
            
            with open(result_file, 'r') as f:
                content = f.read()
            
            # Parse and highlight key values
            import re
            vqe_match = re.search(r'VQE Ground State Energy: (.*)', content)
            exact_match = re.search(r'Exact Energy: (.*)', content)
            error_match = re.search(r'Error: (.*)', content)
            
            if vqe_match and exact_match:
                vqe_energy = vqe_match.group(1)
                exact_energy = exact_match.group(1)
                error = error_match.group(1) if error_match else "N/A"
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-around; margin: 1rem 0;">
                    <div style="text-align: center; padding: 1rem; background: #e1f0fa; border-radius: 10px; flex: 1; margin: 0 0.5rem;">
                        <div style="color: #666; font-size: 0.9rem;">VQE Energy</div>
                        <div style="color: #3498DB; font-size: 1.8rem; font-weight: bold;">{vqe_energy}</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #e1f0fa; border-radius: 10px; flex: 1; margin: 0 0.5rem;">
                        <div style="color: #666; font-size: 0.9rem;">Exact Energy</div>
                        <div style="color: #2980B9; font-size: 1.8rem; font-weight: bold;">{exact_energy}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if error != "N/A":
                    error_float = float(error)
                    color = "#27ae60" if error_float < 0.01 else "#e67e22" if error_float < 0.1 else "#e74c3c"
                    st.markdown(f"""
                    <div style="text-align: center; margin: 1rem 0;">
                        <span style="background: {color}; color: white; padding: 0.5rem 2rem; border-radius: 50px; font-weight: bold;">
                            Error: {error}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.code(content, language="text")
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠ Result file not found. There might be an issue with the calculation.</div>', unsafe_allow_html=True)
        
        # Display convergence plot
        if os.path.exists(convergence_img):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #3498DB; margin-bottom: 1rem;">📈 Energy Convergence</h3>
            """, unsafe_allow_html=True)
            
            image = Image.open(convergence_img)
            st.image(image, use_container_width=True)
            
            # Add interpretation
            st.markdown("""
            <div style="background: #e1f0fa; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <p style="color: #333; margin: 0;"><strong>📌 Analysis:</strong></p>
                <p style="color: #666; margin-top: 0.5rem;">
                • The plot shows VQE energy decreasing with iterations<br>
                • Red dashed line: Exact ground state energy<br>
                • Convergence indicates successful optimization<br>
                • Final energy should closely match exact value
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠ Convergence plot not found. There might be an issue with the calculation.</div>', unsafe_allow_html=True)

# Additional information section (always visible)
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>ℹ About VQE</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #3498DB;">🎯 What is VQE?</h3>
        <p style="color: #666;">Variational Quantum Eigensolver is a hybrid quantum-classical algorithm for finding ground state energies of molecules.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #3498DB;">⚙ Components</h3>
        <p style="color: #666;">• Ansatz: TwoLocal (RY, CZ, 2 repetitions)</p>
        <p style="color: #666;">• Optimizer: COBYLA (100 iterations)</p>
        <p style="color: #666;">• Estimator: StatevectorEstimator</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #3498DB;">📊 Output</h3>
        <p style="color: #666;">• Ground state energy</p>
        <p style="color: #666;">• Comparison with exact solution</p>
        <p style="color: #666;">• Convergence history</p>
    </div>
    """, unsafe_allow_html=True)

# Technical details
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #333; margin: 2rem 0;'>🔬 Technical Specifications</h3>", unsafe_allow_html=True)

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

with tech_col1:
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #3498DB;">Molecule</h4>
        <p style="color: #333; font-size: 1.2rem;">H₂</p>
        <p style="color: #666;">0.74 Å bond length</p>
    </div>
    """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #3498DB;">Ansatz</h4>
        <p style="color: #333; font-size: 1.2rem;">TwoLocal</p>
        <p style="color: #666;">RY, CZ, reps=2</p>
    </div>
    """, unsafe_allow_html=True)

with tech_col3:
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #3498DB;">Optimizer</h4>
        <p style="color: #333; font-size: 1.2rem;">COBYLA</p>
        <p style="color: #666;">100 max iterations</p>
    </div>
    """, unsafe_allow_html=True)

with tech_col4:
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #3498DB;">Basis</h4>
        <p style="color: #333; font-size: 1.2rem;">STO-3G</p>
        <p style="color: #666;">Minimal basis</p>
    </div>
    """, unsafe_allow_html=True)

# Navigation footer (always visible)
st.markdown("---")
col_next1, col_next2, col_next3 = st.columns(3)
with col_next1:
    st.page_link("pages/molecule_to_qubit.py", label="← Previous: Molecule → Qubit", use_container_width=True)
with col_next2:
    st.page_link("pages/quantum_vqe.py", label="→ Next: Quantum VQE", use_container_width=True)
with col_next3:
    st.page_link("pages/dimer.py", label="← Back to Classical", use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #999; font-size: 0.9rem;">
    <p>🛠️  VQE Quantum Solver | Part of the Platinum Energy Level Estimation Project</p>
</div>
""", unsafe_allow_html=True)
