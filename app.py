import streamlit as st
import os
import sys
import subprocess

# --- Page Config ---
st.set_page_config(page_title="Lunar Lander AI", page_icon="🚀", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ─── Base & Background ─── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #070b14;
    color: #c8d6e5;
}

[data-testid="stAppViewContainer"] > .main {
    background: radial-gradient(ellipse at 20% 10%, #0a1628 0%, #070b14 60%),
                radial-gradient(ellipse at 80% 90%, #0d1f38 0%, #070b14 60%);
    background-color: #070b14;
}

/* Animated star field via pseudo-element on body */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 40%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 8%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 25%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 55%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 88% 12%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 70%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 80%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 75%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 35% 60%, rgba(255,220,100,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 70% 35%, rgba(180,220,255,0.4) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1525 0%, #080d1a 100%);
    border-right: 1px solid rgba(255, 170, 0, 0.15);
}

[data-testid="stSidebar"] * {
    font-family: 'Space Mono', monospace !important;
}

/* ─── Typography ─── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #ffc13b !important;
    letter-spacing: -0.02em;
}

p, li, div {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.7;
}

/* ─── Tabs ─── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid rgba(255, 170, 0, 0.2);
    gap: 4px;
}

[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700;
    font-size: 0.9rem;
    color: #6b7fa3 !important;
    background: transparent !important;
    border: none !important;
    padding: 10px 20px !important;
    border-radius: 8px 8px 0 0 !important;
    letter-spacing: 0.03em;
    transition: all 0.2s ease;
}

[data-testid="stTabs"] button[role="tab"]:hover {
    color: #ffc13b !important;
    background: rgba(255, 193, 59, 0.05) !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #ffc13b !important;
    background: rgba(255, 193, 59, 0.08) !important;
    border-bottom: 2px solid #ffc13b !important;
}

/* ─── Metrics ─── */
[data-testid="stMetric"] {
    background: rgba(255, 193, 59, 0.06);
    border: 1px solid rgba(255, 193, 59, 0.2);
    border-radius: 10px;
    padding: 12px 16px;
    transition: border-color 0.2s;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(255, 193, 59, 0.45);
}

[data-testid="stMetricLabel"] {
    color: #6b7fa3 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stMetricValue"] {
    color: #ffc13b !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ─── Divider ─── */
hr {
    border-color: rgba(255, 170, 0, 0.15) !important;
}

/* ─── Alerts / Info Boxes ─── */
[data-testid="stAlert"] {
    border-radius: 10px;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem;
    border-left-width: 3px;
}

/* ─── Buttons ─── */
[data-testid="stButton"] > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
    background: linear-gradient(135deg, #ff4b4b 0%, #c0392b 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 24px !important;
    width: 100%;
    box-shadow: 0 4px 20px rgba(255, 75, 75, 0.3);
    transition: all 0.2s ease !important;
    position: relative;
    overflow: hidden;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(255, 75, 75, 0.5) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ─── Video ─── */
video {
    border-radius: 12px;
    border: 1px solid rgba(255, 193, 59, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

/* ─── Warning/Error/Success ─── */
[data-testid="stNotification"] {
    font-family: 'Space Mono', monospace !important;
    border-radius: 10px;
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #070b14; }
::-webkit-scrollbar-thumb { background: rgba(255, 193, 59, 0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 193, 59, 0.5); }
</style>
""", unsafe_allow_html=True)


# ─── Helper: Inline SVG Rocket (fixes the broken image "0" issue) ───
ROCKET_SVG = """
<div style="display:flex; justify-content:center; align-items:center; padding: 20px 0 10px 0;">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 160" width="90" height="120">
    <defs>
      <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#c8d6e5;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#8fa8c0;stop-opacity:1" />
      </linearGradient>
      <linearGradient id="flameGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" style="stop-color:#ffc13b;stop-opacity:1" />
        <stop offset="60%" style="stop-color:#ff6b35;stop-opacity:0.9" />
        <stop offset="100%" style="stop-color:#ff4b4b;stop-opacity:0" />
      </linearGradient>
      <filter id="glow">
        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
        <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
    </defs>
    <!-- Flame -->
    <ellipse cx="60" cy="132" rx="10" ry="22" fill="url(#flameGrad)" filter="url(#glow)" opacity="0.9">
      <animate attributeName="ry" values="18;26;20;28;18" dur="0.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.9;1;0.8;1;0.9" dur="0.3s" repeatCount="indefinite"/>
    </ellipse>
    <!-- Fins -->
    <polygon points="38,110 25,130 45,118" fill="#4a6080" opacity="0.9"/>
    <polygon points="82,110 95,130 75,118" fill="#4a6080" opacity="0.9"/>
    <!-- Body -->
    <rect x="44" y="55" width="32" height="65" rx="4" fill="url(#bodyGrad)"/>
    <!-- Nose cone -->
    <polygon points="60,10 44,55 76,55" fill="#c8d6e5"/>
    <!-- Window -->
    <circle cx="60" cy="80" r="10" fill="#070b14" stroke="#ffc13b" stroke-width="2"/>
    <circle cx="60" cy="80" r="6" fill="#0d2040"/>
    <circle cx="57" cy="77" r="2" fill="rgba(255,193,59,0.5)"/>
    <!-- Detail lines -->
    <line x1="52" y1="65" x2="68" y2="65" stroke="rgba(255,193,59,0.3)" stroke-width="1"/>
    <line x1="52" y1="100" x2="68" y2="100" stroke="rgba(255,193,59,0.3)" stroke-width="1"/>
  </svg>
</div>
"""

# ─── Sidebar ───
with st.sidebar:
    # Render inline SVG rocket — no external URL, no broken image "0"
    st.markdown(ROCKET_SVG, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom:16px;">
        <span style="font-family:'Syne',sans-serif; font-size:1.2rem; font-weight:800;
                     color:#ffc13b; letter-spacing:0.05em;">LUNAR LANDER AI</span><br/>
        <span style="font-family:'Space Mono',monospace; font-size:0.65rem;
                     color:#4a6080; letter-spacing:0.15em; text-transform:uppercase;">
            Reinforcement Learning Demo
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <p style="font-family:'Space Mono',monospace; font-size:0.7rem; color:#6b7fa3;
              text-transform:uppercase; letter-spacing:0.12em; margin-bottom:8px;">
        ⚙️ Technical Specifications
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(255,193,59,0.05); border:1px solid rgba(255,193,59,0.15);
                border-radius:8px; padding:12px 14px; margin-bottom:8px;">
        <div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#6b7fa3;
                    text-transform:uppercase; letter-spacing:0.1em;">Algorithm</div>
        <div style="font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700;
                    color:#c8d6e5;">Deep Q-Network (DQN)</div>
    </div>
    <div style="background:rgba(255,193,59,0.05); border:1px solid rgba(255,193,59,0.15);
                border-radius:8px; padding:12px 14px;">
        <div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#6b7fa3;
                    text-transform:uppercase; letter-spacing:0.1em;">Environment</div>
        <div style="font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700;
                    color:#c8d6e5;">LunarLander-v3</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <p style="font-family:'Space Mono',monospace; font-size:0.7rem; color:#6b7fa3;
              text-transform:uppercase; letter-spacing:0.12em; margin-bottom:8px;">
        📈 Performance Benchmarks
    </p>
    """, unsafe_allow_html=True)

    st.metric(label="v1 (Pro) Score", value="214.79")
    st.metric(label="v2 (Elite) Score", value="267.00", delta="+52.21 Improvement")

    st.divider()

    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; padding:4px 0;">
        <span style="font-size:1.4rem;">👨‍💻</span>
        <div>
            <div style="font-family:'Space Mono',monospace; font-size:0.65rem;
                        color:#4a6080; text-transform:uppercase; letter-spacing:0.1em;">Developer</div>
            <div style="font-family:'Syne',sans-serif; font-size:0.9rem;
                        font-weight:700; color:#c8d6e5;">Syed Imad Muzaffar</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Hero Header ───
st.markdown("""
<div style="padding: 32px 0 8px 0;">
    <h1 style="font-family:'Syne',sans-serif !important; font-size:2.6rem; font-weight:800;
               color:#ffc13b !important; letter-spacing:-0.03em; margin:0; line-height:1.1;">
        🚀 Lunar Lander AI
    </h1>
    <p style="font-family:'Space Mono',monospace; color:#4a6080; font-size:0.82rem;
              margin-top:6px; letter-spacing:0.05em;">
        A Deep Q-Network agent trained to land autonomously on the lunar surface.
    </p>
</div>
""", unsafe_allow_html=True)


# ─── Tabs ───
tab1, tab2 = st.tabs(["🤖  AI Model Evolution", "🎮  Human Challenge"])


# ═══════════════════════════════════════════
# TAB 1 — AI Model Evolution
# ═══════════════════════════════════════════
with tab1:

    st.markdown("""
    <div style="margin: 24px 0 20px 0;">
        <h2 style="font-family:'Syne',sans-serif !important; font-size:1.55rem; font-weight:700;
                   color:#ffc13b !important; margin:0 0 6px 0;">
            ▶️ Evolution of an Autonomous Pilot
        </h2>
        <p style="font-family:'Space Mono',monospace; color:#6b7fa3; font-size:0.8rem; margin:0;">
            Comparing training iterations — Version 2 (Elite) demonstrates superior
            fuel conservation and trajectory precision.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Progress bar visual ──
    st.markdown("""
    <div style="display:flex; align-items:center; gap:16px; margin-bottom:28px;
                background:rgba(255,193,59,0.04); border:1px solid rgba(255,193,59,0.12);
                border-radius:12px; padding:16px 20px;">
        <div style="flex:1;">
            <div style="font-family:'Space Mono',monospace; font-size:0.68rem;
                        color:#4a6080; text-transform:uppercase; letter-spacing:0.1em;
                        margin-bottom:6px;">Training Progress</div>
            <div style="background:rgba(255,255,255,0.05); border-radius:4px; height:6px; overflow:hidden;">
                <div style="background:linear-gradient(90deg,#ffc13b,#ff6b35);
                            width:82%; height:100%; border-radius:4px;
                            box-shadow:0 0 10px rgba(255,193,59,0.5);"></div>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800;
                        color:#ffc13b;">500K</div>
            <div style="font-family:'Space Mono',monospace; font-size:0.65rem;
                        color:#4a6080;">total steps</div>
        </div>
        <div style="width:1px; height:40px; background:rgba(255,193,59,0.2);"></div>
        <div style="text-align:right;">
            <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800;
                        color:#4ecdc4;">+24.5%</div>
            <div style="font-family:'Space Mono',monospace; font-size:0.65rem;
                        color:#4a6080;">score gain</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("""
        <div style="background:rgba(255,193,59,0.05); border:1px solid rgba(255,193,59,0.2);
                    border-radius:12px; padding:16px 20px; margin-bottom:14px;
                    display:flex; align-items:center; gap:12px;">
            <span style="font-size:2rem;">🥉</span>
            <div>
                <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700;
                            color:#c8d6e5;">v1: Pro Agent</div>
                <div style="font-family:'Space Mono',monospace; font-size:0.75rem;
                            color:#ffc13b;">Score: +214.79 &nbsp;·&nbsp; 100K steps</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if os.path.exists("landing_v1_pro.mp4"):
            st.video("landing_v1_pro.mp4")
        else:
            st.markdown("""
            <div style="background:rgba(255,170,0,0.08); border:1px solid rgba(255,170,0,0.25);
                        border-radius:10px; padding:14px 18px; font-family:'Space Mono',monospace;
                        font-size:0.78rem; color:#ffc13b;">
                ⚠️ &nbsp;<code>landing_v1_pro.mp4</code> not found in working directory.
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:rgba(255,193,59,0.08); border:1px solid rgba(255,193,59,0.35);
                    border-radius:12px; padding:16px 20px; margin-bottom:14px;
                    display:flex; align-items:center; gap:12px;
                    box-shadow:0 0 20px rgba(255,193,59,0.1);">
            <span style="font-size:2rem;">🥇</span>
            <div>
                <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700;
                            color:#ffc13b;">v2: Elite Agent</div>
                <div style="font-family:'Space Mono',monospace; font-size:0.75rem;
                            color:#ffc13b;">Score: +267.00 &nbsp;·&nbsp; 500K steps</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if os.path.exists("landing_v2_elite.mp4"):
            st.video("landing_v2_elite.mp4")
        else:
            st.markdown("""
            <div style="background:rgba(255,170,0,0.08); border:1px solid rgba(255,170,0,0.25);
                        border-radius:10px; padding:14px 18px; font-family:'Space Mono',monospace;
                        font-size:0.78rem; color:#ffc13b;">
                ⚠️ &nbsp;<code>landing_v2_elite.mp4</code> not found in working directory.
            </div>
            """, unsafe_allow_html=True)

    # ── How it works section ──
    st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <h3 style="font-family:'Syne',sans-serif !important; font-size:1.15rem; font-weight:700;
               color:#ffc13b !important; margin-bottom:16px;">
        How the Agent Learns
    </h3>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("🧠", "Neural Network", "Multi-layer perceptron maps 8 observations to 4 actions"),
        ("💾", "Replay Buffer", "50K transitions stored; random sampling breaks correlations"),
        ("🎯", "ε-Greedy Policy", "Starts at 100% exploration, anneals to 2% exploitation"),
        ("📉", "Bellman Updates", "γ = 0.99 future discount; target network updated every 250 steps"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,193,59,0.04); border:1px solid rgba(255,193,59,0.12);
                        border-radius:12px; padding:16px; height:100%; text-align:center;
                        transition:border-color 0.2s;">
                <div style="font-size:1.8rem; margin-bottom:8px;">{icon}</div>
                <div style="font-family:'Syne',sans-serif; font-size:0.85rem; font-weight:700;
                            color:#c8d6e5; margin-bottom:6px;">{title}</div>
                <div style="font-family:'Space Mono',monospace; font-size:0.68rem;
                            color:#4a6080; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════
# TAB 2 — Human Challenge
# ═══════════════════════════════════════════
with tab2:

    st.markdown("""
    <div style="margin: 24px 0 20px 0;">
        <h2 style="font-family:'Syne',sans-serif !important; font-size:1.55rem; font-weight:700;
                   color:#ffc13b !important; margin:0 0 6px 0;">
            🎮 Manual Flight Simulation
        </h2>
        <p style="font-family:'Space Mono',monospace; color:#6b7fa3; font-size:0.8rem; margin:0;">
            Test your piloting skills against the AI's efficiency.
            The physics engine is strictly Newtonian.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Controls reference ──
    st.markdown("""
    <div style="background:rgba(78,205,196,0.05); border:1px solid rgba(78,205,196,0.2);
                border-radius:12px; padding:16px 22px; margin-bottom:24px;
                display:flex; flex-wrap:wrap; gap:16px; align-items:center;">
        <span style="font-family:'Space Mono',monospace; font-size:0.68rem; color:#4ecdc4;
                     text-transform:uppercase; letter-spacing:0.12em; flex-shrink:0;">Controls</span>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <kbd style="background:#1a2540; border:1px solid rgba(78,205,196,0.3); color:#c8d6e5;
                        border-radius:6px; padding:4px 10px; font-family:'Space Mono',monospace;
                        font-size:0.75rem;">SPACE</kbd>
            <span style="color:#4a6080; font-size:0.75rem; font-family:'Space Mono',monospace;">Start</span>
            <kbd style="background:#1a2540; border:1px solid rgba(78,205,196,0.3); color:#c8d6e5;
                        border-radius:6px; padding:4px 10px; font-family:'Space Mono',monospace;
                        font-size:0.75rem;">↑</kbd>
            <span style="color:#4a6080; font-size:0.75rem; font-family:'Space Mono',monospace;">Main Thruster</span>
            <kbd style="background:#1a2540; border:1px solid rgba(78,205,196,0.3); color:#c8d6e5;
                        border-radius:6px; padding:4px 10px; font-family:'Space Mono',monospace;
                        font-size:0.75rem;">← →</kbd>
            <span style="color:#4a6080; font-size:0.75rem; font-family:'Space Mono',monospace;">Side Thrusters</span>
            <kbd style="background:#1a2540; border:1px solid rgba(78,205,196,0.3); color:#c8d6e5;
                        border-radius:6px; padding:4px 10px; font-family:'Space Mono',monospace;
                        font-size:0.75rem;">ESC</kbd>
            <span style="color:#4a6080; font-size:0.75rem; font-family:'Space Mono',monospace;">Exit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    IS_CLOUD = sys.platform.startswith('linux')

    if IS_CLOUD:
        st.markdown("""
        <div style="background:rgba(255,193,59,0.06); border:1px solid rgba(255,193,59,0.25);
                    border-left:4px solid #ffc13b; border-radius:0 12px 12px 0;
                    padding:18px 22px; margin-bottom:16px;">
            <div style="font-family:'Syne',sans-serif; font-size:1rem; font-weight:700;
                        color:#ffc13b; margin-bottom:6px;">🌐 Cloud Environment Detected</div>
            <div style="font-family:'Space Mono',monospace; font-size:0.78rem; color:#8a9ab5;
                        line-height:1.7;">
                Interactive real-time physics simulations are unavailable in the browser
                due to hardware and latency constraints. To play, clone the repository and run
                <code style="background:rgba(255,255,255,0.08); padding:2px 6px;
                             border-radius:4px; color:#ffc13b;">streamlit run app.py</code>
                locally.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style="font-family:'Space Mono',monospace; font-size:0.78rem; color:#6b7fa3;
                  margin:16px 0 10px 0;">
            Below: a recorded human gameplay attempt. Notice how difficult it is to balance
            thrust and gravity compared to the trained AI.
        </p>
        """, unsafe_allow_html=True)

        if os.path.exists("human_gameplay.gif"):
            st.image("human_gameplay.gif", use_container_width=True)
        else:
            st.markdown("""
            <div style="background:rgba(255,75,75,0.08); border:1px solid rgba(255,75,75,0.25);
                        border-radius:10px; padding:14px 18px; font-family:'Space Mono',monospace;
                        font-size:0.78rem; color:#ff6b6b;">
                ❌ &nbsp;<code>human_gameplay.gif</code> missing — upload it to your repository.
            </div>
            """, unsafe_allow_html=True)

    else:
        # ── Local mode ──
        if 'sim_active' not in st.session_state:
            st.session_state.sim_active = False

        if st.session_state.sim_active:
            st.markdown("""
            <div style="background:rgba(78,205,196,0.08); border:1px solid rgba(78,205,196,0.3);
                        border-radius:12px; padding:18px 22px; margin-bottom:16px;
                        display:flex; align-items:center; gap:14px;">
                <span style="font-size:1.6rem;">✅</span>
                <div>
                    <div style="font-family:'Syne',sans-serif; font-size:1rem; font-weight:700;
                                color:#4ecdc4;">Flight System Operational</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.75rem;
                                color:#6b7fa3;">Check your taskbar for the Lunar Lander window.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("↩ Reset Dashboard View"):
                st.session_state.sim_active = False
                st.rerun()

        else:
            if st.button("🚀 Launch Flight Simulator"):
                st.session_state.sim_active = True

                sim_code = """
import gymnasium as gym
import pygame
import numpy as np
import sys
import os

def main():
    if sys.platform == 'win32':
        import ctypes
        myappid = 'syedimad.lunarlander.simulator.1'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass

    pygame.init()
    pygame.display.set_caption("Lunar Lander: Manual Override")

    icon_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(icon_surf, (255, 255, 255), (16, 16), 14)
    pygame.draw.polygon(icon_surf, (255, 75, 75), [(16, 6), (8, 22), (24, 22)])
    pygame.display.set_icon(icon_surf)

    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24, bold=True)
    large_font = pygame.font.SysFont('Arial', 40, bold=True)

    env = gym.make("LunarLander-v3", render_mode="rgb_array")
    obs, info = env.reset()

    done = False
    waiting_for_start = True
    total_reward = 0.0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and waiting_for_start:
                    waiting_for_start = False
                elif event.key == pygame.K_ESCAPE:
                    done = True

        action = 0
        if not waiting_for_start:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]: action = 2
            elif keys[pygame.K_LEFT]: action = 1
            elif keys[pygame.K_RIGHT]: action = 3

            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            if terminated or truncated:
                done = True

        frame = env.render()
        surf = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))
        screen.blit(surf, (0, 0))

        score_color = (0, 255, 0) if total_reward >= 0 else (255, 100, 100)
        score_text = font.render(f"SCORE: {total_reward:.1f}", True, score_color)
        screen.blit(score_text, (20, 20))

        if waiting_for_start:
            txt = large_font.render("PRESS SPACE TO START", True, (255, 255, 0))
            rect = txt.get_rect(center=(300, 200))
            pygame.draw.rect(screen, (0, 0, 0), rect.inflate(30, 20))
            screen.blit(txt, rect)

        pygame.display.flip()
        clock.tick(30)

    screen.fill((20, 20, 30))
    msg = large_font.render("SIMULATION COMPLETE", True, (255, 255, 255))
    s1 = font.render(f"Your Final Score: {total_reward:.1f}", True, score_color)
    s2 = font.render("AI Elite Benchmark: 267.0", True, (0, 255, 255))
    screen.blit(msg, msg.get_rect(center=(300, 130)))
    screen.blit(s1, s1.get_rect(center=(300, 200)))
    screen.blit(s2, s2.get_rect(center=(300, 250)))
    pygame.display.flip()
    pygame.time.wait(4000)

    env.close()
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
"""
                with open("lander_sim.py", "w") as f:
                    f.write(sim_code)

                subprocess.Popen([sys.executable, "lander_sim.py"])
                st.rerun()
