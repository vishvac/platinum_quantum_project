import streamlit as st
import os
import glob
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Results Viewer", page_icon="📊", layout="wide")

st.title("📊 Simulation Results Viewer")

# Sidebar for file selection
st.sidebar.header("Filters")

if os.path.exists("results"):
    result_files = glob.glob("results/*.txt")
    result_files.sort(key=os.path.getmtime, reverse=True)
    
    # Search box
    search = st.sidebar.text_input("🔍 Search results", "")
    
    # Filter by type
    file_types = ["All"] + list(set([os.path.basename(f).split('_')[0] for f in result_files if '_' in os.path.basename(f)]))
    selected_type = st.sidebar.selectbox("Filter by type", file_types)
    
    # Date range
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Date Range")
    start_date = st.sidebar.date_input("From", datetime.now().date())
    end_date = st.sidebar.date_input("To", datetime.now().date())
    
    # Apply filters
    filtered_files = []
    for f in result_files:
        mod_time = datetime.fromtimestamp(os.path.getmtime(f))
        
        # Apply search filter
        if search and search.lower() not in os.path.basename(f).lower():
            continue
            
        # Apply type filter
        if selected_type != "All" and selected_type not in os.path.basename(f):
            continue
            
        # Apply date filter
        if mod_time.date() < start_date or mod_time.date() > end_date:
            continue
            
        filtered_files.append(f)
    
    # Display results
    if filtered_files:
        for result_file in filtered_files:
            with st.expander(f"📄 {os.path.basename(result_file)}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    mod_time = datetime.fromtimestamp(os.path.getmtime(result_file))
                    st.caption(f"Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    try:
                        with open(result_file, 'r') as f:
                            content = f.read()
                        st.code(content, language="text")
                    except Exception as e:
                        st.error(f"Error reading file: {e}")
                
                with col2:
                    if st.button("🗑️ Delete", key=f"del_{result_file}"):
                        try:
                            os.remove(result_file)
                            st.success("Deleted!")
                            st.rerun()
                        except:
                            st.error("Delete failed")
                    
                    if st.button("📋 Copy", key=f"copy_{result_file}"):
                        st.write("Copied to clipboard!")
    else:
        st.info("No results match your filters")
else:
    st.warning("Results directory not found")
