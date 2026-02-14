import streamlit as st
import pandas as pd
from data_processor import load_data, get_data_info
from llm_handler import generate_visualization_proposals, step3_generate_plotting_code
from visualization import generate_plotly_visualization
from utils import validate_dataframe
from dotenv import load_dotenv
import plotly.express as px
import traceback
import datetime

load_dotenv()

st.set_page_config(page_title="Intelligent Data Viz", layout="wide")

st.title("🎨 Intelligent Data Visualization App")
st.markdown("""
Upload a CSV dataset, ask a business question, and get **AI-generated visualizations** with justifications.
Uses a **multi-step LLM scaffolding approach** for smart chart recommendations.
""")

# Sidebar for instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. **Upload** a CSV file
    2. **Ask** a business question
    3. **Review** 3 AI-proposed visualizations
    4. **Select** your favorite
    5. **Download** as PNG
    """)
    st.markdown("---")
    st.markdown("**Example Questions:**")
    st.markdown("- What factors influence housing prices?")
    st.markdown("- Show the distribution of sales by region")
    st.markdown("- How do age and income correlate?")

# Main content
uploaded_file = st.file_uploader("📁 Upload your CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Load and validate data
        with st.spinner("Loading your data..."):
            df = load_data(uploaded_file)
            
            if df is None or df.empty:
                st.error("The uploaded file appears to be empty. Please check your file.")
            else:
                validate_dataframe(df)

                # Display data info
                with st.expander("📊 Dataset Overview", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Rows", df.shape[0])
                        st.metric("Columns", df.shape[1])
                    with col2:
                        st.write("**Column Names:**")
                        st.code(", ".join(df.columns))
                    
                    st.dataframe(df.head(10), use_container_width=True)

                # User question
                st.markdown("---")
                question = st.text_input(
                    "❓ What would you like to visualize?", 
                    placeholder="e.g., What factors influence housing prices?",
                    help="Ask a business question about your data"
                )

                if st.button("🚀 Generate Visualizations", type="primary", key="generate_btn") and question:
                    # Clear previous results
                    if 'figs' in st.session_state:
                        del st.session_state['figs']
                    
                    # Store in session state to persist across reruns
                    with st.spinner("🧠 Analyzing dataset and question..."):
                        try:
                            # Get data info
                            data_info = get_data_info(df)

                            # Generate proposals using multi-step approach
                            proposals = generate_visualization_proposals(question, data_info, 3)
                            
                            # Store in session state
                            st.session_state['proposals'] = proposals
                            st.session_state['data_info'] = data_info
                            st.session_state['df'] = df
                        except Exception as e:
                            st.error(f"Error generating proposals: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())

                # Display proposals if they exist
                if 'proposals' in st.session_state:
                    proposals = st.session_state['proposals']
                    data_info = st.session_state['data_info']
                    df = st.session_state['df']
            
                    st.markdown("---")
                    st.subheader("📈 AI-Generated Visualization Proposals")
                    
                    # Show step 1 analysis
                    if proposals and 'step1_analysis' in proposals[0]:
                        st.info(f"**Column Analysis:** {proposals[0]['step1_analysis']}")
            
                    # Create tabs for each proposal
                    tabs = st.tabs([f"Option {i+1}: {proposal['viz_type'].capitalize()}" for i, proposal in enumerate(proposals)])
            
                    # Initialize or retrieve figs from session state
                    if 'figs' not in st.session_state or len(st.session_state.get('figs', [])) != 3:
                        st.session_state['figs'] = []
                        
                        for i, (tab, proposal) in enumerate(zip(tabs, proposals)):
                            with tab:
                                # Display justification
                                st.markdown(f"**📝 Justification:** {proposal['justification']}")
                                
                                if 'columns_to_use' in proposal:
                                    st.markdown(f"**🔧 Columns:** {', '.join(proposal['columns_to_use'])}")
                                
                                # Generate visualization
                                try:
                                    with st.spinner(f"Generating {proposal['viz_type']} chart..."):
                                        # Generate code using step 3
                                        code = step3_generate_plotting_code(proposal, data_info)
                                        
                                        # Execute the generated code
                                        local_vars = {'df': df, 'px': px}
                                        exec(code, {'px': px, 'df': df, 'pd': pd}, local_vars)
                                        fig = local_vars.get('fig')
                                        
                                        if fig:
                                            st.plotly_chart(fig, use_container_width=True, key=f"viz_{i}")
                                            st.session_state['figs'].append(fig)
                                        else:
                                            # Fallback to simple visualization
                                            fig = generate_plotly_visualization(
                                                df, 
                                                proposal['viz_type'],
                                                proposal.get('columns_to_use', [None, None])[0] if 'columns_to_use' in proposal else None,
                                                proposal.get('columns_to_use', [None, None])[1] if 'columns_to_use' in proposal and len(proposal['columns_to_use']) > 1 else None
                                            )
                                            st.plotly_chart(fig, use_container_width=True, key=f"viz_{i}")
                                            st.session_state['figs'].append(fig)
                                            
                                except Exception as e:
                                    st.error(f"⚠️ Error generating visualization: {str(e)}")
                                    # Try fallback
                                    try:
                                        fig = generate_plotly_visualization(
                                            df, 
                                            proposal['viz_type'],
                                            proposal.get('columns_to_use', [None, None])[0] if 'columns_to_use' in proposal else None,
                                            proposal.get('columns_to_use', [None, None])[1] if 'columns_to_use' in proposal and len(proposal['columns_to_use']) > 1 else None
                                        )
                                        st.plotly_chart(fig, use_container_width=True, key=f"viz_fallback_{i}")
                                        st.session_state['figs'].append(fig)
                                    except Exception as e2:
                                        st.error(f"Fallback also failed: {str(e2)}")
                                        st.session_state['figs'].append(None)
                    else:
                        # Display existing figs
                        for i, (tab, proposal) in enumerate(zip(tabs, proposals)):
                            with tab:
                                st.markdown(f"**📝 Justification:** {proposal['justification']}")
                                if 'columns_to_use' in proposal:
                                    st.markdown(f"**🔧 Columns:** {', '.join(proposal['columns_to_use'])}")
                                if st.session_state['figs'][i]:
                                    st.plotly_chart(st.session_state['figs'][i], use_container_width=True, key=f"viz_display_{i}")
            
                    figs = st.session_state['figs']
            
                    # Selection and download
                    st.markdown("---")
                    st.subheader("💾 Select & Download")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        selected = st.radio(
                            "Choose a visualization to download:",
                            options=[f"Option {i+1}: {proposals[i]['viz_type'].capitalize()}" for i in range(3)],
                            index=0,
                            horizontal=True,
                            key="viz_selector"
                        )
                    
                    selected_idx = int(selected.split()[1].rstrip(':')) - 1
                    
                    with col2:
                        if figs[selected_idx]:
                            try:
                                # Generate unique filename with timestamp to avoid caching
                                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = f"viz_{proposals[selected_idx]['viz_type']}_{timestamp}.png"
                                
                                # Download button with unique key based on selection
                                img_bytes = figs[selected_idx].to_image(format='png', width=1200, height=800)
                                st.download_button(
                                    label="⬇️ Download PNG",
                                    data=img_bytes,
                                    file_name=filename,
                                    mime="image/png",
                                    key=f"download_btn_{selected_idx}"  # Unique key per option
                                )
                            except Exception as e:
                                st.error(f"Download error: {str(e)}")
                                st.info("Try installing kaleido: pip install kaleido==0.2.1")
                        else:
                            st.warning("Figure not available for download")

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        import traceback
        with st.expander("Show error details"):
            st.code(traceback.format_exc())

else:
    # Landing state
    st.info("👆 Upload a CSV or Excel file to get started!")
