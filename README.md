# 🌌 Advanced AI Image Creation Studio

A high-fidelity, professional AI image generation platform built with a modern **Glassmorphism UI**. This studio leverages **Stable Diffusion 3.5** via **Qubrid AI** to transform text prompts into breathtaking visual assets.

## ✨ Features
* **Premium Glass UI:** Frosted glass components with deep purple Qubrid-inspired accents.
* **Dual-View Logic:** Optimized landing page with curated styles and a focused "Studio Workspace" for active generations.
* **Curated Style Templates:** One-click generation for Cyberpunk, Fantasy, Portraiture, and Isometric styles.
* **Advanced State Management:** Uses **LangGraph** to manage generation workflows and history.
* **One-Click Assets:** Integrated high-resolution PNG download for every generation.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Custom Glass CSS)
* **Orchestration:** LangGraph & LangChain
* **AI Model:** Stable Diffusion 3.5 (via Qubrid API)
* **Database:** SQLite (for session and message persistence)
* **Environment:** Python 3.12+ (Managed by `uv`)

## 🚀 Getting Started

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/advanced-ai-image-creation.git](https://github.com/YOUR_USERNAME/advanced-ai-image-creation.git)
   cd advanced-ai-image-creation
Setup Environment:
Create a .env file and add your Qubrid API key:

Code snippet
QUBRID_API_KEY=your_key_here
Install & Run:

Bash
uv run streamlit run frontend/app.py

---

### 4. Git Commands to Push Changes
Run these commands in your terminal to sync all your recent frontend and backend work to GitHub:

```bash
# Stage all changes (Styles, Sidebar, App, and Logic fixes)
git add .

# Commit with a professional message
git commit -m "feat: complete UI overhaul to Advanced AI Image Studio with Glassmorphism and Qubrid branding"

# Push to your new repository name
git push origin main