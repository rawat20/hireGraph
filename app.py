import streamlit as st
from backend import app_graph

st.set_page_config(page_title="Latex Resume Optimizer", layout="wide")

st.title("📄 Overleaf/LaTeX Resume Optimizer")
st.markdown("Paste your **LaTeX code** and the **Job Description**.")

# Layout: Two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Job Description")
    jd_text = st.text_area("Paste JD here...", height=400)

with col2:
    st.subheader("2. Your LaTeX Code")
    latex_input = st.text_area("Paste LaTeX code here...", height=400)

# Run Button
if st.button("✨ Optimize Resume"):
    if not jd_text or not latex_input:
        st.error("Please provide both the JD and the LaTeX code.")
    else:
        # Initialize State
        initial_state = {
            "job_description": jd_text,
            "original_latex": latex_input,
            "revision_count": 0,
            "score": 0,
            "feedback": "",
            "optimized_latex": ""
        }
        
        # Create the status container
        status = st.status("🚀 Agents are working...", expanded=True)
        
        try:
            # Run Graph
            final_state = initial_state
            
            # Stream events
            for event in app_graph.stream(initial_state):
                for key, value in event.items():
                    if key == "editor":
                        status.write(f"✍️ **Draft {value['revision_count']} generated...**")
                        final_state.update(value)
                    elif key == "evaluator":
                        status.write(f"🧐 **Critique Score: {value['score']}/10** - {value['feedback']}")
                        final_state.update(value)
            
            # IF SUCCESSFUL:
            status.update(label="✅ Optimization Complete!", state="complete", expanded=False)
            
            # Display Results
            st.divider()
            st.subheader("3. Optimized LaTeX Code")
            st.info("Copy the code below into Overleaf.")
            st.code(final_state["optimized_latex"], language="latex")
            
            with st.expander("See Optimization Feedback"):
                st.write(f"**Final Score:** {final_state['score']}/10")
                st.write(f"**AI Critique:** {final_state['feedback']}")

        except Exception as e:
            # IF ERROR: Stop spinner and show error state
            status.update(label="❌ An error occurred", state="error", expanded=True)
            st.error(f"System Error: {str(e)}")
            st.warning("Tip: Check your API Key in .env and ensure you have access to Google Gemini.")