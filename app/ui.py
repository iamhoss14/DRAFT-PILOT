import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="DraftPilot | AI Suite", page_icon="✨", layout="centered")

# Custom CSS for polished inputs and clean card styling
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 16px !important; border-radius: 10px !important; padding: 12px !important; }
    .stButton>button { border-radius: 8px !important; font-weight: 600 !important; }
    .history-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ DraftPilot")
st.markdown("Your intelligent copywriting suite backed by persistent storage.")

# Initialize Session State
if "generated_text" not in st.session_state:
    st.session_state.generated_text = None

# Navigation Tabs
tab_create, tab_history = st.tabs(["✍️ Draft Workspace", "📚 My Content"])

# --- TAB 1: DRAFT WORKSPACE ---
with tab_create:
    st.markdown("Specify your parameters to generate publication-ready dispatches.")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        content_type = st.selectbox("Content Type", [
            "Blog Post", "Email", "LinkedIn Post", 
            "Instagram Caption", "Product Description", "Marketing Copy"
        ])
    with col2:
        tone = st.selectbox("Tone", [
            "Professional", "Friendly", "Persuasive", 
            "Casual", "Technical", "Creative"
        ])
    with col3:
        length = st.selectbox("Length", ["Short", "Medium", "Long"])
    with col4:
        language = st.selectbox("Language", ["English", "Persian", "Spanish", "French", "German"])

    topic = st.text_area("Topic", placeholder='"How AI is transforming software engineering..."', height=100)

    def fetch_content():
        if not topic.strip():
            st.warning("⚠️ Please provide a subject matter before proceeding.")
            return
            
        with st.status("Executing prompt and logging to database...", expanded=True) as status:
            try:
                payload = {
                    "content_type": content_type,
                    "topic": topic,
                    "tone": tone,
                    "length": length,
                    "language": language
                }
                response = requests.post("http://127.0.0.1:8000/generate", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.generated_text = data['content']
                    status.update(label="Complete and Saved to PostgreSQL!", state="complete", expanded=False)
                elif response.status_code == 429:
                    status.update(label="Limit Reached", state="error")
                    st.error("🛑 Daily quota reached. Please try again tomorrow.")
                else:
                    status.update(label="Error", state="error")
                    st.error(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                status.update(label="Error", state="error")
                st.error(f"Could not connect to FastAPI backend. Error: {str(e)}")

    if st.button("Generate 🚀", type="primary", use_container_width=True):
        fetch_content()

    if st.session_state.generated_text:
        st.divider()
        st.subheader("📄 Active Document")
        st.code(st.session_state.generated_text, language="markdown")
        
        if st.button("Regenerate 🔄", use_container_width=True):
            fetch_content()

# --- TAB 2: MY CONTENT (HISTORY) ---
with tab_history:
    st.subheader("📚 Saved Generations")
    st.caption("All dispatches recorded in your PostgreSQL database.")
    
    col_ref, _ = st.columns([1, 3])
    with col_ref:
        if st.button("Refresh History 🔄", use_container_width=True):
            st.rerun()

    try:
        response = requests.get("http://127.0.0.1:8000/generations")
        if response.status_code == 200:
            generations = response.json()
            
            if not generations:
                st.info("No saved records found. Draft your first piece in the workspace!")
            else:
                for item in generations:
                    created_time = datetime.fromisoformat(item["created_at"]).strftime("%B %d, %Y - %H:%M")
                    
                    with st.expander(f"{item['content_type']} — {created_time}"):
                        st.caption(f"**Record ID:** {item['id']}")
                        st.code(item["content"], language="markdown")
                        
                        col_del, _ = st.columns([1, 4])
                        with col_del:
                            if st.button("Delete 🗑️", key=f"del_{item['id']}", use_container_width=True):
                                del_res = requests.delete(f"http://127.0.0.1:8000/generations/{item['id']}")
                                if del_res.status_code == 200:
                                    st.success("Entry deleted.")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete record.")
        else:
            st.error(f"Failed to fetch history (Status {response.status_code})")
    except Exception as e:
        st.error(f"Could not connect to database backend: {str(e)}")