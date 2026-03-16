import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: #ffffff;
    }
    
    /* Back button styling - Fixed position on all pages */
    .back-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        background: white;
        color: #667eea;
        padding: 10px 20px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        z-index: 999;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        transition: all 0.3s;
        border: 1px solid rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(10px);
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .back-btn:hover {
        transform: translateX(-5px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
    }
    
    .back-btn::before {
        content: "←";
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* Graph card styling */
    .graph-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .graph-card::before {
        content: "📊";
        position: absolute;
        font-size: 5rem;
        opacity: 0.1;
        right: 10px;
        bottom: 10px;
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecf5 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        width: 100%;
        border: 1px solid transparent;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric card styling */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #eef2f6;
        transition: all 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.1);
        border-color: #667eea;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
        line-height: 1.2;
    }
    
    .metric-label {
        color: #666;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: #f8f9fa;
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        padding: 12px 24px;
        color: #666;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Success/Error message styling */
    .stAlert {
        border-radius: 12px;
        border-left: 6px solid #667eea;
        padding: 1rem;
        font-weight: 500;
    }
    
    /* Code block styling */
    .stCode {
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border: 1px solid #eef2f6;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .stMarkdown {
        color: white;
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: #333;
        font-weight: 700;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: #333;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.8rem;
        white-space: nowrap;
        z-index: 1000;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #eef2f6;
    }
    
    .dataframe th {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px;
    }
    
    .dataframe td {
        padding: 10px;
        background: white;
    }
    
    /* Card container */
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        padding: 20px 0;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        background: #f0f3ff;
        color: #667eea;
        margin: 0 5px 5px 0;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
