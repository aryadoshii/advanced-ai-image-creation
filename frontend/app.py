import streamlit as st
import sys
import os
import time
import base64

# Path setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.graph import build_graph
from database.db import init_db, create_session, get_history
from frontend.sidebar import render_sidebar
from frontend.styles import get_css
from config.settings import GENERATED_IMAGES_DIR

# --- INITIALIZATION ---
init_db()
os.makedirs(GENERATED_IMAGES_DIR, exist_ok=True)

st.set_page_config(
    page_title="Advanced AI Image Creation",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "current_session_id" not in st.session_state:
    st.session_state["current_session_id"] = None
if "auto_prompt" not in st.session_state:
    st.session_state["auto_prompt"] = None

# Inject Glass CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Custom CSS for Inputs
st.markdown("""
<style>
    /* Hide the "Press Enter" text */
    [data-testid="InputInstructions"] { display: none !important; }
    
    /* Hide Labels */
    .stTextInput label { display: none; }
    
    /* Glass Input Box */
    .stTextInput input {
        border-radius: 12px 0 0 12px !important;
        padding: 15px 20px !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        font-size: 1.1rem !important;
    }
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* Send Button */
    div[data-testid="stForm"] button {
        border-radius: 0 12px 12px 0 !important;
        height: 52px;
        background-color: #6366f1 !important;
        border: none !important;
        color: white !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stForm"] button:hover {
        background-color: #4f46e5 !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
    }
    div[data-testid="stForm"] { border: none; padding: 0; }
    
    .stImage img { border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.4); }
</style>
""", unsafe_allow_html=True)

render_sidebar()

# --- LOGIC HELPERS ---

def run_generation(session_id, user_prompt):
    """Handles the AI generation process with UI feedback."""
    with st.status("⚡ Quantum rendering in progress...", expanded=True) as status:
        st.write("Initializing Stable Diffusion 3.5...")
        prog = st.progress(20)
        time.sleep(0.3)
        
        st.write("Enhancing prompt acoustics...")
        prog.progress(40)
        
        graph = build_graph()
        result = graph.invoke({
            "session_id": session_id,
            "user_prompt": user_prompt,
            "generated_image_url": None,
            "error": None
        })
        
        prog.progress(100)
        status.update(label="✨ Creation Complete!", state="complete", expanded=False)
        return result

def get_download_link(img_path):
    try:
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'<a href="data:image/png;base64,{b64}" download="art.png" class="glass-card" style="display:inline-block; padding:10px 20px; text-decoration:none; color:white; margin-top:10px; font-size:0.9rem;">⬇️ Download High-Res</a>'
    except: return ""

# --- VIEW 1: LANDING PAGE ---
def show_landing_page():
    # Hero Title
    st.markdown("""
        <div style="text-align: center; padding: 60px 20px 20px 20px;">
            <div class="hero-title">Advanced AI<br>Image Creation</div>
            <div class="hero-subtitle">
                Transform your imagination into breathtaking visuals with our professional AI studio. 
                Optimized for Game Assets, Concept Art, and Photorealism.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 1. INSPIRATION GRID (Now First)
    st.markdown("<h4 style='text-align:center; color:rgba(255,255,255,0.5); margin-bottom: 20px;'>🔥 Curated Styles</h4>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    def card(col, title, img, prompt):
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <img src="{img}" style="width:100%; height:180px; object-fit:cover; opacity:0.8;">
                <div style="padding:15px;">
                    <div style="font-weight:bold; margin-bottom:5px;">{title}</div>
                    <div style="font-size:0.8rem; color:rgba(255,255,255,0.6);">Click to Generate</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Create", key=f"btn_{title}", use_container_width=True):
                st.session_state["auto_prompt"] = prompt
                session_id = create_session(title=prompt)
                st.session_state["current_session_id"] = session_id
                st.rerun()

    # --- NEW RELIABLE IMAGE LINKS ---
    # Cyberpunk: Neon City Night
    card(c1, "Cyberpunk", "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=600&q=80", "Cyberpunk city, neon, rain, 8k")
    # Fantasy: Dark Castle
    card(c2, "Fantasy", "https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?w=600&q=80", "Epic fantasy castle, magic, clouds")
    # Portrait: Futuristic Face
    card(c3, "Portrait", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=600&q=80", "Cinematic portrait, detailed skin, 85mm")
    # Isometric: 3D Room
    card(c4, "Isometric", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&q=80", "Isometric cute magic shop, 3d render, blender")

    # 2. CENTERED INPUT (Now Below Grid)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        with st.form(key="landing_form", border=False):
            c_input, c_btn = st.columns([5, 1], gap="small")
            with c_input:
                landing_prompt = st.text_input("Landing", placeholder="✨ Describe your vision...")
            with c_btn:
                submitted = st.form_submit_button("➤", use_container_width=True)

            if submitted and landing_prompt:
                session_id = create_session(title=landing_prompt)
                st.session_state["current_session_id"] = session_id
                st.session_state["auto_prompt"] = landing_prompt
                st.rerun()


# --- VIEW 2: WORKSPACE ---
def show_workspace():
    st.markdown("## 🎨 Studio Workspace")
    
    # 1. Show History
    history = get_history(st.session_state["current_session_id"])
    for msg in history:
        if msg['role'] == 'user':
            st.markdown(f"""<div class="user-msg"><div>👤</div><div>{msg['content']}</div></div>""", unsafe_allow_html=True)
        else:
            if msg['image_url'] and os.path.exists(msg['image_url']):
                st.image(msg['image_url']) 
                st.markdown(get_download_link(msg['image_url']), unsafe_allow_html=True)
                st.markdown("<div style='margin-bottom:30px'></div>", unsafe_allow_html=True)

    # 2. Handle Auto-Trigger (First generation from landing)
    if st.session_state.get("auto_prompt"):
        p = st.session_state["auto_prompt"]
        st.session_state["auto_prompt"] = None # Clear immediately
        st.markdown(f"""<div class="user-msg"><div>👤</div><div>{p}</div></div>""", unsafe_allow_html=True)
        res = run_generation(st.session_state["current_session_id"], p)
        if res.get("generated_image_url"): 
            st.rerun()

    # 3. Chat Input
    prompt = st.chat_input("Describe your vision...")
    if prompt:
        st.markdown(f"""<div class="user-msg"><div>👤</div><div>{prompt}</div></div>""", unsafe_allow_html=True)
        res = run_generation(st.session_state["current_session_id"], prompt)
        if res.get("generated_image_url"): 
            st.rerun()


# --- MAIN CONTROLLER ---
if st.session_state["current_session_id"] is None:
    show_landing_page()
else:
    show_workspace()