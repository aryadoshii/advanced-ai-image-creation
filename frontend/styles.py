def get_css():
    """
    Returns the 'Qubrid Dark Glass' CSS with STATIC Background.
    """
    return """
    <style>
        /* --- IMPORTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        /* --- STATIC BACKGROUND (No Animation) --- */
        .stApp {
            /* Deep, rich, static background matching Qubrid/SeaArt */
            background: radial-gradient(circle at 50% 10%, #1a103c 0%, #050505 60%, #000000 100%);
            background-attachment: fixed;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        /* --- REMOVE DEFAULT HEADER --- */
        header[data-testid="stHeader"] { background: transparent !important; }

        /* --- SIDEBAR GLASS --- */
        [data-testid="stSidebar"] {
            background-color: rgba(5, 5, 10, 0.6) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* --- GLASS CARDS --- */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 0;
            overflow: hidden;
            transition: transform 0.3s ease, border-color 0.3s, box-shadow 0.3s;
            height: 100%;
        }

        .glass-card:hover {
            transform: translateY(-5px);
            border-color: rgba(138, 43, 226, 0.6);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        }

        /* --- HERO TITLE (WHITE & STATIC) --- */
        .hero-title {
            font-size: 5rem;
            font-weight: 900;
            color: #FFFFFF !important;
            text-shadow: 0 0 50px rgba(138, 43, 226, 0.3); /* Static Purple Glow */
            letter-spacing: -0.03em;
            line-height: 1.1;
            margin-bottom: 2rem; 
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 400;
            line-height: 1.6;
            margin-bottom: 3rem;
        }

        /* --- CHAT BUBBLES --- */
        .user-msg {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 20px;
            backdrop-filter: blur(5px);
            margin-bottom: 20px;
            display: flex; gap: 15px; align-items: flex-start;
        }

        /* --- BUTTONS --- */
        .stButton button {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 12px;
            transition: all 0.2s;
        }
        .stButton button:hover {
            background: rgba(138, 43, 226, 0.2); /* Static Purple Hover */
            border-color: #8a2be2;
            color: #ffffff;
        }

        /* --- HIDE DEFAULT UI ELEMENTS --- */
        [data-testid="InputInstructions"] { display: none !important; }
        footer { display: none !important; }
        #MainMenu { display: none !important; }
    </style>
    """