import streamlit as st
import requests

# 1. Page Config
st.set_page_config(page_title="DraftPilot | AI Writer", page_icon="✨", layout="centered")

# 2. Safe, Modern CSS that respects Dark/Light Mode
st.markdown("""
    <style>
    /* Clean up the text area for maximum readability */
    .stTextArea textarea {
        font-size: 16px !important;
        border-radius: 10px !important;
        padding: 16px !important;
        line-height: 1.5;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Sleek subtext styling */
    .header-subtext {
        font-size: 1.1rem;
        color: #888;
        margin-top: -15px;
        margin-bottom: 25px;
        font-weight: 300;
    }
    
    /* Better button spacing */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Modern Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("Fine-tune the AI output.")
    
    tone = st.selectbox("Tone", ["Executive", "Conversational", "Technical", "Direct", "Creative"])
    format_type = st.selectbox("Format", ["Article", "Email", "Strategic Brief", "Social Post"])
    
    st.divider()
    st.caption("Engine: FastAPI | Model: Gemini 3.8-Flash")

# 4. Main UI Header
st.title("✨ DraftPilot AI")
st.markdown('<div class="header-subtext">Your intelligent drafting assistant.</div>', unsafe_allow_html=True)

# 5. Input Area
topic = st.text_area(
    "What are we working on today?",
    placeholder="Type your topic here... (e.g., A technical overview of API rate limiting)",
    height=150
)

# 6. Action Button & Logic
if st.button("Generate Content 🚀", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("⚠️ Please enter a topic to begin.")
    else:
        # Beautiful loading state
        with st.status("Processing your request...", expanded=True) as status:
            st.write("Initiating secure connection...")
            st.write("Drafting content with Gemini...")
            
            try:
                payload = {"topic": topic, "tone": tone, "format_type": format_type}
                response = requests.post("http://127.0.0.1:8000/generate", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    status.update(label="Document Ready!", state="complete", expanded=False)
                    
                    # Clean display of remaining limits
                    st.success(f"API Requests Remaining Today: **{data['remaining_requests']} / 2**")
                    
                    # Premium output container
                    st.subheader("📄 Generated Document")
                    with st.container(border=True):
                        st.write(data['result'])
                        
                elif response.status_code == 429:
                    status.update(label="Limit Reached", state="error")
                    st.error("🛑 Daily capacity reached. Please try again tomorrow.")
                else:
                    status.update(label="System Error", state="error")
                    st.error(f"Failed to generate: Error {response.status_code}")
                    
            except Exception as e:
                status.update(label="Connection Error", state="error")
                st.error(f"Could not connect to the backend. Ensure FastAPI is running! Error: {str(e)}")