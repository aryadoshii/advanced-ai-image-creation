import streamlit as st
import sys
import os
import time
import base64

# Path setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import init_db, create_session, get_history, get_sessions
from frontend.sidebar import render_sidebar
from frontend.styles import get_css
from backend.graph import build_graph
from config.settings import API_KEY, GENERATED_IMAGES_DIR

# --- INITIALIZATION ---
init_db()
os.makedirs(GENERATED_IMAGES_DIR, exist_ok=True)

st.set_page_config(
    page_title="Advanced AI Image Creation",
    page_icon="https://www.qubrid.com/favicon.ico", 
    layout="wide",
    initial_sidebar_state="expanded"
)

if "current_session_id" not in st.session_state:
    st.session_state["current_session_id"] = None
if "auto_prompt" not in st.session_state:
    st.session_state["auto_prompt"] = None

# Inject Global Glassmorphism CSS
st.markdown(get_css(), unsafe_allow_html=True)

# CSS to stop the "Dark Fading" during generation
st.markdown("""
<style>
    /* Keeps the UI bright and prevents darkening during generation */
    .st-emotion-cache-6qob1r { 
        background-color: transparent !important; 
    }
    
    /* Makes the generation status box clear and glass-like */
    [data-testid="stStatusWidget"] { 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        backdrop-filter: blur(10px); 
    }
</style>
""", unsafe_allow_html=True)

# --- HELPERS ---
def run_generation(session_id, user_prompt):
    # This status block will now be transparent thanks to the CSS above
    with st.status("⚡ Quantum rendering in progress...", expanded=True) as status:
        st.write("Initializing Stable Diffusion 3.5...")
        prog = st.progress(20)
        time.sleep(0.3)
        graph = build_graph()
        result = graph.invoke({"session_id": session_id, "user_prompt": user_prompt, "generated_image_url": None, "error": None})
        prog.progress(100)
        status.update(label="✨ Creation Complete!", state="complete", expanded=False)
        return result

def get_download_link(img_path):
    try:
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'<a href="data:image/png;base64,{b64}" download="art.png" class="download-btn">⬇️ Download High-Res</a>'
    except: return ""

# --- RENDER SIDEBAR ---
render_sidebar()

# ==========================================
# VIEW CONTROLLER
# ==========================================

# CASE 1: LANDING PAGE (Only show if no session is active)
if st.session_state["current_session_id"] is None:
    
    # 1. Landing Hero
    st.markdown("""
        <div style="text-align: center; padding: 60px 20px 20px 20px;">
            <div class="hero-title">Advanced AI<br>Image Creation</div>
            <div class="hero-subtitle">
                Transform your imagination into breathtaking visuals with our professional AI studio. 
                Optimized for Game Assets, Concept Art, and Photorealism using <b>Stable Diffusion 3.5</b>.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Local CSS for Landing UI
    st.markdown("""
    <style>
    .stTextInput input {
        height: 48px !important;
        border-radius: 12px !important;
        padding: 0 18px !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: white !important;
    }
    div[data-testid="stForm"] button {
        height: 44px !important;
        width: 44px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important;
        color: white !important;
        display: flex; align-items: center; justify-content: center;
    }
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    # 3. Curated Styles Grid
    st.markdown("<h4 style='text-align:center; color:rgba(255,255,255,0.5); margin-bottom: 20px;'>🔥 Curated Styles</h4>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    def card(col, title, img, prompt):
        with col:
            st.markdown(f'<div class="glass-card"><img src="{img}" style="width:100%; height:180px; object-fit:cover; opacity:0.8;"><div style="padding:15px;"><div style="font-weight:bold; margin-bottom:5px;">{title}</div></div></div>', unsafe_allow_html=True)
            if st.button("Create", key=f"btn_{title}", use_container_width=True):
                # Start session and trigger generation
                new_id = create_session(title=prompt)
                st.session_state["current_session_id"] = new_id
                st.session_state["auto_prompt"] = prompt
                st.rerun()

    card(c1, "Cyberpunk", "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=600&q=80", "Cyberpunk city, neon, rain, 8k")
    card(c2, "Fantasy", "https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?w=600&q=80", "Epic fantasy castle, magic, clouds")
    card(c3, "Portrait", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=600&q=80", "Cinematic portrait, detailed skin, 85mm")
    card(c4, "Isometric", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&q=80", "Isometric cute magic shop, 3d render, blender")

    # 4. Landing Input
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        with st.form(key="landing_form", border=False):
            c_input, c_btn = st.columns([5, 1])
            with c_input:
                landing_prompt = st.text_input("Landing", placeholder="✨ Describe your vision...")
            with c_btn:
                submitted = st.form_submit_button("➤")
            if submitted and landing_prompt:
                new_id = create_session(title=landing_prompt)
                st.session_state["current_session_id"] = new_id
                st.session_state["auto_prompt"] = landing_prompt
                st.rerun()
        st.markdown("<div style='text-align:center; color:rgba(255,255,255,0.3); font-size:0.8rem; margin-top:10px;'>Powered by Qubrid AI</div>", unsafe_allow_html=True)

# CASE 2: STUDIO WORKSPACE (Strictly active only when a session is chosen)
else:
    st.markdown("## 🎨 Studio Workspace")
    
    # 1. History Retrieval
    history = get_history(st.session_state["current_session_id"])
    for msg in history:
        if msg['role'] == 'user':
            st.markdown(f'<div class="user-msg"><div>👤</div><div>{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            if msg['image_url'] and os.path.exists(msg['image_url']):
                st.image(msg['image_url']) 
                st.markdown(get_download_link(msg['image_url']), unsafe_allow_html=True)
                st.markdown("<div style='margin-bottom:30px'></div>", unsafe_allow_html=True)

    # 2. Logic to handle the very first prompt from landing
    if st.session_state.get("auto_prompt"):
        p = st.session_state["auto_prompt"]
        st.session_state["auto_prompt"] = None
        st.markdown(f'<div class="user-msg"><div>👤</div><div>{p}</div></div>', unsafe_allow_html=True)
        res = run_generation(st.session_state["current_session_id"], p)
        if res.get("generated_image_url"): st.rerun()

    # 3. Workspace Chat Input (ChatGPT Style at the bottom)
    prompt = st.chat_input("Describe your vision...")
    if prompt:
        st.markdown(f'<div class="user-msg"><div>👤</div><div>{prompt}</div></div>', unsafe_allow_html=True)
        res = run_generation(st.session_state["current_session_id"], prompt)
        if res.get("generated_image_url"): st.rerun()
    
    st.markdown("<div style='text-align:center; color:rgba(255,255,255,0.2); font-size:0.7rem; margin-top:50px;'>Powered by Qubrid AI</div>", unsafe_allow_html=True)