import streamlit as st
from database.db import get_sessions

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🪐 Studio History")
        
        if st.button("✨ New Creation", type="primary", use_container_width=True):
            st.session_state["current_session_id"] = None
            st.rerun()
            
        st.markdown("---")
            
        sessions = get_sessions()
        if not sessions:
            st.markdown("<div style='color:rgba(255,255,255,0.4); font-size:0.8rem;'>No projects yet.</div>", unsafe_allow_html=True)
            
        for s in sessions:
            title = s['title'][:22] + "..." if len(s['title']) > 25 else s['title']
            is_active = st.session_state.get("current_session_id") == s['id']
            icon = "💠" if is_active else "📄"
            
            # Unique key for every button
            if st.button(f"{icon}  {title}", key=f"sess_{s['id']}", use_container_width=True):
                st.session_state["current_session_id"] = s['id']
                st.rerun()
                
        # Footer
        st.markdown("<div style='margin-top: 50px; color:rgba(255,255,255,0.3); font-size:0.8rem; text-align:center;'>Powered by Qubrid AI</div>", unsafe_allow_html=True)