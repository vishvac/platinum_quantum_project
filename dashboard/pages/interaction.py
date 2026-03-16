import streamlit as st
import subprocess
import os
from PIL import Image
from style import load_css
import glob
import re

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Pt₂ Interaction Energy",
    page_icon="⚡",
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
        color: #96CEB4;
        padding: 10px 20px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        z-index: 999;
        box-shadow: 0 4px 15px rgba(150, 206, 180, 0.2);
        transition: all 0.3s;
        border: 1px solid rgba(150, 206, 180, 0.2);
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
        box-shadow: 0 6px 20px rgba(150, 206, 180, 0.3);
        background: linear-gradient(90deg, #96CEB4 0%, #4ECDC4 100%);
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
        background: linear-gradient(135deg, #96CEB4 0%, #4ECDC4 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(150, 206, 180, 0.3);
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
        background: linear-gradient(90deg, #96CEB4 0%, #4ECDC4 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.3rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(150, 206, 180, 0.3);
    }
    
    .run-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(150, 206, 180, 0.4);
    }
    
    .info-panel {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #96CEB4;
    }
    
    .feature-tag {
        display: inline-block;
        background: #d4e8e0;
        color: #1a4d3e;
        padding: 0.3rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        margin: 0.2rem;
        font-weight: 600;
        border: 1px solid #96CEB4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
    
    .energy-formula {
        background: #f0f7fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-family: monospace;
        margin: 1rem 0;
        color: #000000;
        font-weight: 600;
    }
    
    .result-highlight {
        background: linear-gradient(135deg, #96CEB4 0%, #4ECDC4 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .result-highlight h2 {
        margin: 0;
        font-size: 2rem;
    }
    
    .result-highlight p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
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
    <h1>⚡ Pt₂ Interaction Energy</h1>
    <p>Accurate Interaction Energy: E(Pt₂) - 2E(Pt)</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for tracking if simulation was run
if 'interaction_simulation_run' not in st.session_state:
    st.session_state.interaction_simulation_run = False

# Main content layout
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # Info panel
    st.markdown("""
    <div class="info-panel">
        <h3 style="color: #333; margin-bottom: 1rem;">🔬 Calculation Details</h3>
        <p style="color: #666;">This calculation computes the interaction energy using:</p>
        <div style="margin: 1rem 0;">
            <span class="feature-tag">⚛ def2svp basis</span>
            <span class="feature-tag">🔮 ECP treatment</span>
            <span class="feature-tag">📊 UHF/RHF</span>
            <span class="feature-tag">⚡ Interaction energy</span>
            <span class="feature-tag">📈 PES scan</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Energy formula
    st.markdown("""
    <div class="energy-formula">
        <strong>ΔE = E(Pt₂) - 2 × E(Pt)</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Single atom info
    st.markdown("""
    <div style="background: #f0f3ff; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: #333; margin-bottom: 0.5rem;"><strong>📌 Pt Atom Configuration:</strong></p>
        <p style="color: #666; margin: 0;">[Xe] 4f¹⁴ 5d⁹ 6s¹ • Spin multiplicity: 3 (triplet) • 78 electrons</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add spacer div
    st.markdown('<div class="button-spacer"></div>', unsafe_allow_html=True)
    
    # Run button
    run = st.button("🚀 RUN INTERACTION CALCULATION", key="run_btn", use_container_width=True)

# Handle simulation run
if run:
    st.session_state.interaction_simulation_run = True
    
    with st.container():
        st.markdown('<div class="info-message">⚙ Running interaction energy calculation... This may take a few moments.</div>', unsafe_allow_html=True)
        
        with st.spinner("Calculating Pt atom and Pt₂ dimer energies..."):
            # Run the interaction script
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "calculate_interaction.py")
            result = subprocess.run(["python3", script_path], 
                                   capture_output=True, 
                                   text=True)
            
            if result.returncode == 0:
                st.markdown('<div class="success-message">✅ Calculation completed successfully!</div>', unsafe_allow_html=True)
                
                # Show output in expander
                with st.expander("View calculation output"):
                    st.code(result.stdout, language="bash")
            else:
                st.markdown('<div class="error-message">❌ Calculation failed. Check the error message below.</div>', unsafe_allow_html=True)
                st.code(result.stderr, language="bash")
                st.session_state.interaction_simulation_run = False

# Results section - ONLY show if simulation has been run
if st.session_state.interaction_simulation_run:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>📊 Simulation Results</h2>", unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # Check for result files
        result_file = "results/interaction_final.txt"
        curve_img = "results/pt2_interaction_curve.png"
        
        # Display text results
        if os.path.exists(result_file):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #96CEB4; margin-bottom: 1rem;">📝 Final Results</h3>
            """, unsafe_allow_html=True)
            
            with open(result_file, 'r') as f:
                content = f.read()
            
            # Extract interaction energy for highlight
            interaction_match = re.search(r'Interaction energy.*?= (.*?) Hartree', content)
            if interaction_match:
                interaction_energy = interaction_match.group(1)
                st.markdown(f"""
                <div class="result-highlight">
                    <h2>ΔE = {interaction_energy} Hartree</h2>
                    <p>Pt₂ Interaction Energy</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.code(content, language="text")
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠ Result file not found. There might be an issue with the calculation.</div>', unsafe_allow_html=True)
        
        # Display potential energy curve
        if os.path.exists(curve_img):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #96CEB4; margin-bottom: 1rem;">📈 Potential Energy Curve</h3>
            """, unsafe_allow_html=True)
            
            image = Image.open(curve_img)
            st.image(image, use_container_width=True)
            
            # Add interpretation
            st.markdown("""
            <div style="background: #e8f3ee; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <p style="color: #333; margin: 0;"><strong>📌 Analysis:</strong> The potential energy curve shows the 
                interaction energy as a function of Pt-Pt distance. The minimum represents the equilibrium bond length.</p>
                <p style="color: #666; margin-top: 0.5rem; font-size: 0.9rem;">
                • Scan range: 2.0 - 3.0 Å<br>
                • 21 points calculated<br>
                • Optimal bond length: ~2.33 Å
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠ Potential energy curve not found. There might be an issue with the calculation.</div>', unsafe_allow_html=True)

# Additional information section (always visible)
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>ℹ About Interaction Energy</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #96CEB4;">🎯 Definition</h3>
        <p style="color: #666;">The interaction energy ΔE = E(Pt₂) - 2E(Pt) measures the strength of the Pt-Pt bond.</p>
        <p style="color: #96CEB4; font-weight: bold; margin-top: 1rem;">Negative ΔE = Stable bond</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #96CEB4;">⚙ Components</h3>
        <p style="color: #666;">• Single Pt atom energy (UHF, triplet)</p>
        <p style="color: #666;">• Pt₂ dimer energy (RHF, singlet)</p>
        <p style="color: #666;">• Basis set: def2svp + ECP</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #96CEB4;">📊 Output</h3>
        <p style="color: #666;">• Interaction energy (Hartree, eV, kcal/mol)</p>
        <p style="color: #666;">• Bond dissociation energy Dₑ</p>
        <p style="color: #666;">• Potential energy curve</p>
    </div>
    """, unsafe_allow_html=True)

# Key parameters table
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #333; margin: 2rem 0;'>🔑 Key Parameters</h3>", unsafe_allow_html=True)

param_col1, param_col2, param_col3, param_col4 = st.columns(4)

with param_col1:
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #96CEB4;">Bond Length</h4>
        <p style="color: #333; font-size: 1.2rem;">2.33 Å</p>
        <p style="color: #666; font-size: 0.9rem;">(optimal)</p>
    </div>
    """, unsafe_allow_html=True)

with param_col2:
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #96CEB4;">Spin Multiplicity</h4>
        <p style="color: #333; font-size: 1.2rem;">1 (singlet)</p>
        <p style="color: #666; font-size: 0.9rem;">Pt₂ ground state</p>
    </div>
    """, unsafe_allow_html=True)

with param_col3:
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #96CEB4;">Pt Configuration</h4>
        <p style="color: #333; font-size: 1.2rem;">5d⁹ 6s¹</p>
        <p style="color: #666; font-size: 0.9rem;">triplet atom</p>
    </div>
    """, unsafe_allow_html=True)

with param_col4:
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #96CEB4;">ECP</h4>
        <p style="color: #333; font-size: 1.2rem;">def2svp</p>
        <p style="color: #666; font-size: 0.9rem;">relativistic</p>
    </div>
    """, unsafe_allow_html=True)

# Navigation footer (always visible)
st.markdown("---")
col_next1, col_next2, col_next3 = st.columns(3)
with col_next1:
    st.page_link("pages/dimer.py", label="← Previous: Pt₂ Dimer", use_container_width=True)
with col_next2:
    st.page_link("pages/cluster.py", label="← Previous: Pt₄ Cluster", use_container_width=True)
with col_next3:
    st.page_link("pages/surface.py", label="← Previous: Pt Surface", use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #999; font-size: 0.9rem;">
    <p>⚡ Pt₂ Interaction Energy Analysis | Part of the Platinum Energy Level Estimation Project</p>
</div>
""", unsafe_allow_html=True)
