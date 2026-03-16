import streamlit as st
import subprocess
import os
from PIL import Image
from style import load_css
import glob

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Pt Surface Simulation",
    page_icon="🌐",
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
        color: #45B7D1;
        padding: 10px 20px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        z-index: 999;
        box-shadow: 0 4px 15px rgba(69, 183, 209, 0.2);
        transition: all 0.3s;
        border: 1px solid rgba(69, 183, 209, 0.2);
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
        box-shadow: 0 6px 20px rgba(69, 183, 209, 0.3);
        background: linear-gradient(90deg, #45B7D1 0%, #4ECDC4 100%);
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
        background: linear-gradient(135deg, #45B7D1 0%, #4ECDC4 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(69, 183, 209, 0.3);
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
        background: linear-gradient(90deg, #45B7D1 0%, #4ECDC4 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.3rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(69, 183, 209, 0.3);
    }
    
    .run-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(69, 183, 209, 0.4);
    }
    
    .info-panel {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #45B7D1;
    }
    
    .feature-tag {
        display: inline-block;
        background: #e1f0f5;
        color: #45B7D1;
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
    
    .surface-visualization {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 1rem;
    }
    
    .layer-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .layer-1 { background: #ff6b6b; color: white; }
    .layer-2 { background: #4ecdc4; color: white; }
    .layer-3 { background: #ffd93d; color: #333; }
    
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
    <h1>🌐 Platinum Surface Model</h1>
    <p>10-Atom Slab for Catalysis Studies</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for tracking if simulation was run
if 'surface_simulation_run' not in st.session_state:
    st.session_state.surface_simulation_run = False

# Main content layout
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    # Info panel
    st.markdown("""
    <div class="info-panel">
        <h3 style="color: #333; margin-bottom: 1rem;">🔬 Simulation Details</h3>
        <p style="color: #666;">This calculation analyzes a platinum surface model using:</p>
        <div style="margin: 1rem 0;">
            <span class="feature-tag">⚛ def2svp basis</span>
            <span class="feature-tag">🔮 ECP treatment</span>
            <span class="feature-tag">📊 DFT (PBE)</span>
            <span class="feature-tag">🌐 2-layer slab</span>
            <span class="feature-tag">📈 Density of States</span>
        </div>
        <p style="color: #666; margin-top: 1rem;"><strong>System size:</strong> 10 Pt atoms (2 layers + extra atoms)</p>
        <p style="color: #666;"><strong>Layer spacing:</strong> 2.24 Å between layers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Layer visualization
    st.markdown("""
    <div style="background: #f0f7fa; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: #333; margin-bottom: 0.5rem;"><strong>📌 Layer Structure:</strong></p>
        <div>
            <span class="layer-badge layer-1">Layer 1: Surface (4 atoms)</span>
            <span class="layer-badge layer-2">Layer 2: Subsurface (4 atoms)</span>
            <span class="layer-badge layer-3">Bottom Layer (2 atoms)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add spacer div
    st.markdown('<div class="button-spacer"></div>', unsafe_allow_html=True)
    
    # Run button
    run = st.button("🚀 RUN SURFACE CALCULATION", key="run_btn", use_container_width=True)

# Handle simulation run
if run:
    st.session_state.surface_simulation_run = True
    
    with st.container():
        st.markdown('<div class="info-message">⚙ Running surface calculation... This may take a few moments.</div>', unsafe_allow_html=True)
        
        with st.spinner("Running DFT calculation on Pt surface model..."):
            # Run the surface script
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "platinum_surface.py")
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
                st.session_state.surface_simulation_run = False

# Results section - ONLY show if simulation has been run
if st.session_state.surface_simulation_run:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>📊 Simulation Results</h2>", unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        # Check for result files
        result_file = "results/surface_final.txt"
        structure_img = "results/pt_surface_model.png"
        dos_img = "results/pt_surface_dos.png"
        
        # Display text results
        if os.path.exists(result_file):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #45B7D1; margin-bottom: 1rem;">📝 Final Results</h3>
            """, unsafe_allow_html=True)
            
            with open(result_file, 'r') as f:
                content = f.read()
            st.code(content, language="text")
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠ Result file not found. There might be an issue with the calculation.</div>', unsafe_allow_html=True)
        
        # Display surface structure
        if os.path.exists(structure_img):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #45B7D1; margin-bottom: 1rem;">📈 Surface Structure Visualization</h3>
            """, unsafe_allow_html=True)
            
            image = Image.open(structure_img)
            st.image(image, use_container_width=True)
            
            # Add interpretation
            st.markdown("""
            <div class="surface-visualization">
                <p style="color: #333; margin: 0;"><strong>📌 Analysis:</strong> The 10-atom surface model shows 
                the atomic arrangement of a platinum catalyst surface.</p>
                <p style="color: #666; margin-top: 0.5rem; font-size: 0.9rem;">
                • <span style="color: #ff6b6b;">Blue: Layer 1 (Surface)</span> - Primary catalytic sites<br>
                • <span style="color: #4ecdc4;">Green: Layer 2</span> - Subsurface atoms<br>
                • <span style="color: #ffd93d;">Yellow: Bottom Layer</span> - Support layer
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Display DOS plot if available
        if os.path.exists(dos_img):
            st.markdown("""
            <div class="result-container">
                <h3 style="color: #45B7D1; margin-bottom: 1rem;">📊 Density of States</h3>
            """, unsafe_allow_html=True)
            
            dos_image = Image.open(dos_img)
            st.image(dos_image, use_container_width=True)
            
            st.markdown("""
            <div class="surface-visualization">
                <p style="color: #333; margin: 0;"><strong>📌 Electronic Structure:</strong> The DOS shows the 
                distribution of electronic states near the Fermi level, crucial for catalytic activity.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# Additional information section (always visible)
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: #333; margin: 2rem 0;'>ℹ About This Calculation</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #45B7D1;">🎯 Purpose</h3>
        <p style="color: #666;">Model platinum catalyst surfaces to understand adsorption sites and electronic properties relevant to catalysis.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #45B7D1;">⚙ Methods</h3>
        <p style="color: #666;">DFT with PBE functional, def2svp basis set, and effective core potential (ECP) for relativistic effects.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); height: 100%;">
        <h3 style="color: #45B7D1;">📊 Output</h3>
        <p style="color: #666;">Total energy, energy per atom, density of states (DOS), and surface layer analysis.</p>
    </div>
    """, unsafe_allow_html=True)

# Applications section
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #333; margin: 2rem 0;'>🔬 Catalytic Applications</h3>", unsafe_allow_html=True)

app_col1, app_col2, app_col3, app_col4 = st.columns(4)

with app_col1:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #45B7D1;">H₂ Adsorption</h4>
        <p style="color: #666;">Hydrogen dissociation</p>
    </div>
    """, unsafe_allow_html=True)

with app_col2:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #45B7D1;">CO Oxidation</h4>
        <p style="color: #666;">Catalytic converters</p>
    </div>
    """, unsafe_allow_html=True)

with app_col3:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #45B7D1;">O₂ Activation</h4>
        <p style="color: #666;">Oxygen reduction</p>
    </div>
    """, unsafe_allow_html=True)

with app_col4:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: #45B7D1;">Fuel Cells</h4>
        <p style="color: #666;">Energy conversion</p>
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
    st.page_link("pages/interaction.py", label="→ Next: Interaction", use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #999; font-size: 0.9rem;">
    <p>🌐 Platinum Surface Model | Part of the Platinum Energy Level Estimation Project</p>
</div>
""", unsafe_allow_html=True)
