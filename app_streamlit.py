"""
NIXIN AI - Layer 1 Context Engine
Streamlit Web Interface
"""

import streamlit as st
import json
from datetime import datetime
from nlp_engine import analyze_input
from reasoning_engine import reason
from action_engine import execute

# Page configuration
st.set_page_config(
    page_title="NIXIN AI - Context Engine",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5em;
        margin-bottom: 1em;
    }
    .intent-badge {
        display: inline-block;
        padding: 0.5em 1em;
        border-radius: 0.5em;
        font-weight: bold;
        margin: 0.5em 0;
    }
    .intent-schedule {
        background-color: #A23B72;
        color: white;
    }
    .intent-reminder {
        background-color: #F18F01;
        color: white;
    }
    .intent-preference {
        background-color: #C73E1D;
        color: white;
    }
    .intent-retrieve {
        background-color: #6A994E;
        color: white;
    }
    .intent-create {
        background-color: #2E86AB;
        color: white;
    }
    .intent-unknown {
        background-color: #757575;
        color: white;
    }
    .confidence-bar {
        margin-top: 1em;
        margin-bottom: 1em;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🤖 NIXIN AI - Context Engine</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.subheader("Intent Detection")
    intent_backend = st.selectbox(
        "Detection Method",
        ["Rule-Based", "Sentence Transformers", "HuggingFace", "Claude API"]
    )
    
    st.subheader("Memory")
    if st.button("📋 Load Memory"):
        try:
            with open("memory.json", "r") as f:
                memory = json.load(f)
                st.success("Memory loaded!")
                st.json(memory)
        except FileNotFoundError:
            st.warning("No memory file found")
    
    st.subheader("Help")
    st.info("""
    **Try these commands:**
    - "Schedule a meeting tomorrow"
    - "Remind me about the project"
    - "Set my preference to quiet hours"
    - "What did I tell you?"
    - "Send an email to John"
    """)

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Input Your Request")
    user_input = st.text_input(
        "You:",
        placeholder="e.g., Schedule a meeting tomorrow at 3pm",
        label_visibility="collapsed"
    )

with col2:
    st.subheader("Analysis Mode")
    analysis_mode = st.toggle("Show Detailed Analysis", value=True)

if user_input:
    st.markdown("---")
    
    # Analyze input
    intent_data = analyze_input(user_input)
    
    # Display Results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Intent Detected", intent_data["intent"], delta=None)
    
    with col2:
        confidence_pct = f"{int(intent_data['confidence'] * 100)}%"
        st.metric("Confidence", confidence_pct, delta=None)
    
    with col3:
        entity_count = len(intent_data["entities"])
        st.metric("Entities Found", entity_count, delta=None)
    
    st.markdown("---")
    
    # Intent Badge
    intent = intent_data["intent"]
    intent_class_map = {
        "schedule_meeting": "intent-schedule",
        "set_reminder": "intent-reminder",
        "set_preference": "intent-preference",
        "retrieve_task": "intent-retrieve",
        "create_task": "intent-create",
        "unknown": "intent-unknown"
    }
    
    intent_class = intent_class_map.get(intent, "intent-unknown")
    st.markdown(
        f'<div class="intent-badge {intent_class}">{intent.upper().replace("_", " ")}</div>',
        unsafe_allow_html=True
    )
    
    # Confidence Bar
    st.markdown('<div class="confidence-bar">', unsafe_allow_html=True)
    st.progress(float(intent_data["confidence"]))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed Analysis
    if analysis_mode:
        st.subheader("📊 Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Time Entity:**")
            st.code(str(intent_data["time"]) if intent_data["time"] else "None")
        
        with col2:
            st.write("**Person Entity:**")
            st.code(str(intent_data["person"]) if intent_data["person"] else "None")
        
        st.write("**All Entities:**")
        if intent_data["entities"]:
            for entity_text, entity_type in intent_data["entities"]:
                st.caption(f"🏷️ `{entity_text}` → `{entity_type}`")
        else:
            st.caption("No entities found")
    
    st.markdown("---")
    
    # Reasoning Engine
    st.subheader("🧠 Reasoning")
    action_data = reason(intent_data, user_input)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Action Type:**")
        st.code(action_data.get("action", "Unknown"))
    
    with col2:
        st.write("**Reasoning:**")
        st.code(action_data.get("reasoning", "No reasoning available"))
    
    st.markdown("---")
    
    # Action Execution
    st.subheader("⚡ Response")
    response = execute(action_data, user_input)
    
    st.success("✅ Action executed")
    st.info(f"**A:** {response}")
    
    # Metadata
    with st.expander("📋 Metadata"):
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "intent_data": intent_data,
            "action_data": action_data,
            "detection_method": intent_backend
        }
        st.json(metadata)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 0.85em;">
    NIXIN AI - Layer 1 Context Engine | Powered by Transformers & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
