import streamlit as st
import os
import sys
import subprocess

# --- Page Config ---
st.set_page_config(page_title="Lunar Lander AI", page_icon="🚀", layout="wide")

# Custom UI Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h2, h3 { color: #ffaa00; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #FF4B4B; color: white; font-weight: bold; padding: 12px;}
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/OpenAI_Gym_LunarLander.png/320px-OpenAI_Gym_LunarLander.png", use_container_width=True)
    st.header("⚙️ Technical Specifications")
    st.write("**Algorithm:** Deep Q-Network (DQN)")
    st.write("**Environment:** LunarLander-v3")
    
    st.divider()
    st.subheader("📈 Performance Benchmarks")
    st.metric(label="v1 (Pro) Score", value="214.79")
    st.metric(label="v2 (Elite) Score", value="267.00", delta="+52.21 Improvement")
    
    st.divider()
    st.write("👨‍💻 **Developer:** Syed Imad Muzaffar")

# --- Tabs ---
tab1, tab2 = st.tabs(["🤖 AI Model Evolution", "🎮 Human Challenge"])

# --- TAB 1: AI Model Evolution ---
with tab1:
    st.subheader("▶️ Evolution of an Autonomous Pilot")
    st.write("Comparing training iterations: Version 2 (Elite) demonstrates superior fuel conservation and trajectory precision.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🥉 v1: Pro Agent (+214)")
        if os.path.exists("landing_v1_pro.mp4"):
            st.video("landing_v1_pro.mp4")
        else:
            st.warning("Video 'landing_v1_pro.mp4' missing.")
            
    with col2:
        st.markdown("### 🥇 v2: Elite Agent (+267)")
        if os.path.exists("landing_v2_elite.mp4"):
            st.video("landing_v2_elite.mp4")
        else:
            st.warning("Video 'landing_v2_elite.mp4' missing.")

# --- TAB 2: Human Challenge ---
with tab2:
    st.subheader("🎮 Manual Flight Simulation")
    st.write("Test your piloting skills against the AI's efficiency. The physics engine is strictly Newtonian.")
    
    # --- BULLETPROOF HYBRID DEPLOYMENT LOGIC ---
    # Streamlit Cloud uses Linux. Local Asus TUF uses Windows ('win32').
    IS_CLOUD = sys.platform.startswith('linux')
    
    if IS_CLOUD:
        st.warning("🌐 **Cloud Environment Detected:** Interactive real-time physics simulations are disabled in the web browser due to hardware/latency constraints.")
        st.info("💡 **Want to play?** Clone the repository from GitHub and run it locally on your machine (`streamlit run app.py`) to access the Pygame simulator!")
        
        st.write("Below is a recorded attempt of human gameplay. Notice how difficult it is to balance thrust and gravity compared to the trained AI:")
        if os.path.exists("human_gameplay.gif"):
            st.image("human_gameplay.gif", use_container_width=True)
        else:
            st.error("Missing 'human_gameplay.gif' file. Please upload it to your repository.")
            
    else:
        # --- LOCAL EXECUTION MODE ---
        st.info("""
        **Controls:** [SPACE] Start | [UP] Main Thruster | [LEFT/RIGHT] Side Thrusters | [ESC] Exit
        """)

        if 'sim_active' not in st.session_state:
            st.session_state.sim_active = False

        if st.button("🚀 Launch Flight Simulator"):
            st.session_state.sim_active = True
            
            # --- THE ULTIMATE PYGAME SUBPROCESS CODE ---
            sim_code = """
import gymnasium as gym
import pygame
import numpy as np
import sys
import os

def main():
    # --- WINDOWS 11 TASKBAR ICON OVERRIDE HACK ---
    # Forces Windows to treat this as a unique app, respecting our custom icon.
    if sys.platform == 'win32':
        import ctypes
        myappid = 'syedimad.lunarlander.simulator.1'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass

    pygame.init()
    pygame.display.set_caption("Lunar Lander: Manual Override")
    
    # Create Custom Proper Icon
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
            # Write and launch without any complex logic
            with open("lander_sim.py", "w") as f:
                f.write(sim_code)
                
            subprocess.Popen([sys.executable, "lander_sim.py"])
            st.rerun() 

        # Keep UI visible while simulation is "active"
        if st.session_state.sim_active:
            st.success("✅ Flight System Operational. Check your taskbar for the Lunar Lander window.")
            if st.button("Reset Dashboard View"):
                st.session_state.sim_active = False
                st.rerun()