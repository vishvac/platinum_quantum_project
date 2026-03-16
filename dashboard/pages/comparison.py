import streamlit as st
import pandas as pd
from style import load_css

st.set_page_config(
    page_title="Our Project: Classical vs Quantum",
    page_icon="⚛️",
    layout="wide"
)

load_css()

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea, #9b59b6); padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 2.5rem;">🔬 Our Project: Classical vs Quantum</h1>
    <p style="color: #e0e7ff; font-size: 1.2rem;">What We Can Do with Each Approach</p>
</div>
""", unsafe_allow_html=True)

# Simple explanation
st.markdown("""
<div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 2rem;">
    <h3 style="color: #1e293b; margin-top: 0;">🎯 In Our Project:</h3>
    <p style="color: #334155; font-size: 1.1rem;">We study <strong>platinum systems</strong> (Pt₂, Pt₄, Pt surface) using both methods:</p>
    <ul style="color: #334155;">
        <li><strong style="color: #2563eb;">Classical:</strong> Calculate energies, bond lengths, HOMO-LUMO gaps</li>
        <li><strong style="color: #9b59b6;">Quantum:</strong> Simulate the same on qubits, explore future possibilities</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ===== COMPARISON TABLE SECTION =====
st.markdown("""
<h2 style="color: #1e293b; font-size: 1.8rem; margin: 2rem 0 1rem 0;">📊 Hybrid Quantum vs Fully Classical: Detailed Comparison</h2>
""", unsafe_allow_html=True)

# Comparison data (stars removed)
comparison_data = {
    "Aspect": [
        "Computation Method",
        "Time Complexity",
        "Space Complexity",
        "Accuracy for Strongly Correlated Systems",
        "Scalability",
        "Advantages"
    ],
    "Hybrid Approach (Our Project)": [
        "Combines classical computing with quantum algorithms (e.g., VQE). Classical computers prepare the Hamiltonian and parameters, while the quantum part estimates ground state energy.",
        "Potentially faster for complex quantum systems, because quantum algorithms can explore many quantum states simultaneously.",
        "Uses fewer classical memory resources for representing quantum states because part of the computation is handled by quantum circuits.",
        "Can capture quantum correlations more effectively using quantum circuits.",
        "More scalable for future large quantum chemistry problems when better quantum hardware becomes available.",
        "Combines stability of classical methods and power of quantum computing, reducing computational burden for complex systems."
    ],
    "Fully Classical Approach": [
        "Uses only classical algorithms such as Hartree–Fock or Density Functional Theory for all computations.",
        "Higher time complexity for large molecular systems since classical algorithms must simulate all quantum interactions sequentially.",
        "Requires very large memory to store wavefunctions or matrices for large molecules.",
        "May lose accuracy or become extremely expensive when dealing with strongly correlated electrons.",
        "Limited scalability because computational cost grows rapidly with system size.",
        "Well-established, reliable, and does not require quantum hardware."
    ]
}

# Styling for comparison table
st.markdown("""
<style>
    .comparison-header {
        background: linear-gradient(135deg, #4b5563, #1f2937);
        color: white;
        padding: 1rem;
        border-radius: 10px 10px 0 0;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .hybrid-header {
        background: linear-gradient(135deg, #2563eb, #1e40af);
    }
    .classical-header {
        background: linear-gradient(135deg, #7e22ce, #6b21a8);
    }
    .comparison-row {
        display: flex;
        margin-bottom: 1rem;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .aspect-cell {
        flex: 1.5;
        background: #f8fafc;
        padding: 1.2rem;
        border-right: 1px solid #e2e8f0;
        font-weight: 600;
        color: #0f172a;
    }
    .hybrid-cell {
        flex: 2.5;
        background: linear-gradient(145deg, #f0f9ff, #ffffff);
        padding: 1.2rem;
        border-right: 1px solid #e2e8f0;
        color: #1e293b;
        border-left: 3px solid #2563eb;
    }
    .classical-cell {
        flex: 2.5;
        background: linear-gradient(145deg, #faf5ff, #ffffff);
        padding: 1.2rem;
        color: #1e293b;
        border-left: 3px solid #7e22ce;
    }
    .badge-blue {
        background: #dbeafe;
        color: #1e40af;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.5rem;
        margin-bottom: 0.3rem;
    }
    .badge-purple {
        background: #f3e8ff;
        color: #6b21a8;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.5rem;
        margin-bottom: 0.3rem;
    }
    
    /* Navigation link styling */
    .nav-link {
        color: #667eea !important;
        font-weight: 600;
        text-decoration: none;
        font-size: 1.1rem;
        transition: color 0.3s ease;
    }
    .nav-link:hover {
        color: #9b59b6 !important;
    }
    .section-title {
        color: #1e293b !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header row
col1, col2, col3 = st.columns([1.5, 2.5, 2.5])
with col1:
    st.markdown('<div class="comparison-header">Aspect</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="comparison-header hybrid-header">🚀 Hybrid Approach (Our Project)</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="comparison-header classical-header">🖥️ Fully Classical Approach</div>', unsafe_allow_html=True)

# Data rows
for i in range(len(comparison_data["Aspect"])):
    aspect = comparison_data["Aspect"][i]
    hybrid = comparison_data["Hybrid Approach (Our Project)"][i]
    classical = comparison_data["Fully Classical Approach"][i]
    
    # Add appropriate badges based on aspect
    hybrid_badges = ""
    classical_badges = ""
    
    if "Computation" in aspect:
        hybrid_badges = '<span class="badge-blue">VQE</span> <span class="badge-blue">Qiskit</span> <span class="badge-blue">PySCF+Quantum</span>'
        classical_badges = '<span class="badge-purple">HF</span> <span class="badge-purple">DFT</span> <span class="badge-purple">PySCF</span>'
    elif "Time" in aspect:
        hybrid_badges = '<span class="badge-blue">O(poly(n))</span> <span class="badge-blue">Exponential speedup</span>'
        classical_badges = '<span class="badge-purple">O(N⁴) to O(N⁷)</span> <span class="badge-purple">Exponential wall</span>'
    elif "Space" in aspect:
        hybrid_badges = '<span class="badge-blue">O(n) qubits</span> <span class="badge-blue">2ⁿ states</span>'
        classical_badges = '<span class="badge-purple">O(2ⁿ) memory</span> <span class="badge-purple">TB for 50 qubits</span>'
    elif "Accuracy" in aspect:
        hybrid_badges = '<span class="badge-blue">Captures correlation</span> <span class="badge-blue">99.8%</span>'
        classical_badges = '<span class="badge-purple">Approximations</span> <span class="badge-purple">Expensive for correlation</span>'
    elif "Scalability" in aspect:
        hybrid_badges = '<span class="badge-blue">Future-proof</span> <span class="badge-blue">O(poly(n))</span>'
        classical_badges = '<span class="badge-purple">Limited to ~50 atoms</span> <span class="badge-purple">Hits wall</span>'
    elif "Advantages" in aspect:
        hybrid_badges = '<span class="badge-blue">Best of both</span> <span class="badge-blue">Future-ready</span>'
        classical_badges = '<span class="badge-purple">Mature</span> <span class="badge-purple">Reliable</span> <span class="badge-purple">No quantum needed</span>'
    
    col1, col2, col3 = st.columns([1.5, 2.5, 2.5])
    with col1:
        st.markdown(f'<div class="aspect-cell">{aspect}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="hybrid-cell">{hybrid_badges}<br><br>{hybrid}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="classical-cell">{classical_badges}<br><br>{classical}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# ===== END COMPARISON TABLE =====

# Two columns (original content)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div style="background:white;padding:1.5rem;border-radius:10px;border-left:5px solid #2563eb;box-shadow:0 2px 8px rgba(0,0,0,0.1);height:100%;">
<h2 style="color:#2563eb;">🖥️ Classical Methods</h2>
<h4 style="color:#1e293b;">In Our Code: PySCF, RHF/UHF, DFT</h4>

<p style="color:#1e293b;font-weight:600;">⚡ Efficiency:</p>
<ul style="color:#334155;">
<li><strong>Pt₂ Dimer:</strong> 5-100 ms <span style="background:#e6f7e6;color:#059669;padding:2px 8px;border-radius:12px;">Fast</span></li>
<li><strong>Pt₄ Cluster:</strong> 1-10 seconds <span style="background:#fef3c7;color:#d97706;padding:2px 8px;border-radius:12px;">Medium</span></li>
<li><strong>Pt Surface:</strong> 10-60 seconds <span style="background:#fee2e2;color:#b91c1c;padding:2px 8px;border-radius:12px;">Slow</span></li>
</ul>

<p style="color:#1e293b;font-weight:600;">📊 Time Complexity:</p>
<ul style="color:#334155;">
<li>Pt₂ (2 atoms): <strong>O(10⁴)</strong> operations</li>
<li>Pt₄ (4 atoms): <strong>O(10⁶)</strong> operations</li>
<li>Pt₁₀ (surface): <strong>O(10⁸)</strong> operations</li>
<li>If we try 100 atoms: <span style="color:#b91c1c;">Would take years!</span></li>
</ul>

<p style="color:#1e293b;font-weight:600;">💾 Memory Used:</p>
<ul style="color:#334155;">
<li>Pt₂: <strong>1-5 MB</strong></li>
<li>Pt₄: <strong>10-50 MB</strong></li>
<li>Pt surface: <strong>100-500 MB</strong></li>
<li>100 atoms: <span style="color:#b91c1c;">Would need 10+ TB!</span></li>
</ul>

<div style="background:#dbeafe;padding:1rem;border-radius:8px;margin-top:1rem;">
<p style="color:#1e40af;margin:0;">✅ We can do: Pt₂, Pt₄, Pt₁₀ easily</p>
<p style="color:#1e40af;margin:0;">❌ Can't do: Large platinum clusters (100+ atoms)</p>
</div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background:white;padding:1.5rem;border-radius:10px;border-left:5px solid #9b59b6;box-shadow:0 2px 8px rgba(0,0,0,0.1);height:100%;">
<h2 style="color:#9b59b6;">⚛️ Quantum Methods</h2>
<h4 style="color:#1e293b;">In Our Code: Qiskit, VQE, Jordan-Wigner</h4>

<p style="color:#1e293b;font-weight:600;">⚡ Efficiency:</p>
<ul style="color:#334155;">
<li><strong>H₂ Molecule:</strong> 100-500 ms <span style="background:#fef3c7;color:#d97706;padding:2px 8px;border-radius:12px;">Slower</span></li>
<li><strong>Same as classical?</strong> Yes, but we're learning</li>
<li><strong>Future potential:</strong> <span style="background:#e6f7e6;color:#059669;padding:2px 8px;border-radius:12px;">Exponential speedup</span></li>
</ul>

<p style="color:#1e293b;font-weight:600;">📊 Time Scaling:</p>
<ul style="color:#334155;">
<li>H₂ (2 qubits): <strong>O(10³)</strong> gates</li>
<li>Pt₂ needs: <strong>O(10⁴)</strong> gates</li>
<li>Pt₁₀: <strong>O(10⁶)</strong> gates</li>
<li>Same problem for classical: <span style="color:#b91c1c;">Impossible</span></li>
</ul>

<p style="color:#1e293b;font-weight:600;">🔮 Memory Magic:</p>
<ul style="color:#334155;">
<li>2 qubits = 4 states</li>
<li>20 qubits = 1 million states</li>
<li>100 qubits = <span style="color:#9b59b6;">more states than atoms in universe</span></li>
<li>Stored in just 100 particles</li>
</ul>

<div style="background:#f3e8ff;padding:1rem;border-radius:8px;margin-top:1rem;">
<p style="color:#6b21a8;margin:0;">⚡ We can do now: H₂ (2 qubits)</p>
<p style="color:#6b21a8;margin:0;">🚀 Future potential: Large Pt clusters</p>
</div>
</div>
""", unsafe_allow_html=True)

# Table
st.markdown("""
<h2 style="color: #1e293b; font-size: 1.8rem; margin: 2rem 0 1rem 0;">📊 What Our Project Can Handle</h2>
""", unsafe_allow_html=True)

data = {
    "System": ["H₂ molecule", "Pt₂ dimer", "Pt₄ cluster", "Pt surface (10 atoms)", "Large catalyst (100+ atoms)"],
    "Classical": ["✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "❌ Impossible"],
    "Quantum": ["✅ Yes (learning)", "🔮 Future", "🔮 Future", "🔮 Future", "⚡ Potential!"]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# Bottom message
st.markdown("""
<div style="background: linear-gradient(135deg,#667eea,#9b59b6);padding:2rem;border-radius:15px;text-align:center;margin:2rem 0;">
    <h2 style="color:white;">✨ Why Both Matter in Our Project</h2>
    <p style="color:#e0e7ff;font-size:1.1rem;">🔬 Classical: Simulate Pt₂, Pt₄, Pt surface today</p>
    <p style="color:#e0e7ff;font-size:1.1rem;">⚛️ Quantum: Preparing for future large systems</p>
    <p style="color:white;font-style:italic;">Classical solves today's problems. Quantum prepares tomorrow's discoveries.</p>
</div>
""", unsafe_allow_html=True)

# Navigation with updated colors
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<a href="/" target="_self" style="color: #2563eb; font-weight: 600; text-decoration: none; font-size: 1.1rem; display: block; text-align: center;">← Back to Dashboard</a>', unsafe_allow_html=True)

with col2:
    st.markdown('<a href="/dimer" target="_self" style="color: #2563eb; font-weight: 600; text-decoration: none; font-size: 1.1rem; display: block; text-align: center;">→ Try Pt₂ Dimer</a>', unsafe_allow_html=True)

with col3:
    st.markdown('<a href="/quantum_vqe" target="_self" style="color: #2563eb; font-weight: 600; text-decoration: none; font-size: 1.1rem; display: block; text-align: center;">→ Try Quantum VQE</a>', unsafe_allow_html=True)
