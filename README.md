![Stable Baselines3](https://img.shields.io/badge/Stable_Baselines3-Deep_RL-purple)
![Gymnasium](https://img.shields.io/badge/Gymnasium-LunarLander_v3-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active-success)

# 🚀 Lunar Lander: AI vs Human (Reinforcement Learning)  
**Autonomous Spacecraft Navigation using Deep Q-Networks (DQN)**

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Streamlit-FF4B4B)](https://game-agent-k2.streamlit.app/)

A comprehensive Reinforcement Learning (RL) showcase that trains an autonomous agent to safely navigate a lunar module to a landing pad. The project features a unique **Hybrid Streamlit Dashboard** that not only visualizes the AI's learning evolution but also challenges users to fly the lander manually via a local physics engine, comparing human intuition directly against algorithmic efficiency.

---

## 🛠️ Tech Stack
- **Algorithm:** Deep Q-Network (DQN) with Experience Replay
- **RL Framework:** Stable Baselines3 (PyTorch backend)
- **Physics Environment:** Gymnasium (`LunarLander-v3`)
- **Frontend Dashboard:** Streamlit (Responsive UI, State Management)
- **Local Simulation Engine:** Pygame (Multithreaded Subprocess Integration)
- **Data Processing:** NumPy

---

## 📂 Repository Structure & File Descriptions

```text
Game-Agent/
│
├── app.py                         # Main Streamlit application with Hybrid Environment Logic
├── requirements.txt               # Project dependencies (Streamlit, Stable Baselines3, Gymnasium)
├── README.md                      # Project documentation
│
├── 🧠 Models/
│   ├── dqn_model_v1_pro.zip       # V1 weights (500k steps, Score: +214)
│   └── dqn_model_v2_elite.zip     # V2 weights (Extended training, Score: +267)
│
└── 🎥 Media Assets/
    ├── landing_v1_pro.mp4         # Visual demonstration of the V1 agent
    ├── landing_v2_elite.mp4       # Visual demonstration of the flawless V2 agent
    ├── human_gameplay.gif         # Recording of a human attempting manual flight
    └── random_agent-episode-0.mp4 # Baseline: Shows the chaotic behavior of an UNTRAINED model
```

---

## 📂 Key File Insights

- **random_agent-episode-0.mp4**  
  This file serves as our baseline. It demonstrates how a completely untrained neural network interacts with the environment—firing thrusters randomly, wasting fuel, failing to balance, and ultimately crashing. This starkly contrasts with the precision of the trained agents.

- **dqn_model_v2_elite.zip**  
  The final production model. It has learned the optimal policy to perfectly balance gravity, inertia, and fuel consumption to consistently land flawlessly between the flags.


---

## 🌩️ Hybrid Deployment Architecture (Cloud vs. Local)

One of the major engineering challenges in this project was seamlessly integrating a real-time desktop physics engine (Pygame) with a cloud-hosted web dashboard (Streamlit).

### ⚠️ The Challenge & Consequences

- **Headless Servers:**  
  Cloud platforms (like Streamlit Community Cloud) run on headless Linux servers without physical displays, monitors, or graphic drivers.

- **The Consequence:**  
  If the application attempts to initialize `pygame.display` on the cloud, it throws a fatal SDL exception (Simple DirectMedia Layer error) and crashes the entire web app, completely breaking the user experience.


---

## 🛠️ Our Solution: The Environment-Aware Toggle

To ensure 100% uptime and accessibility, this application utilizes an OS-level environment detection system (`sys.platform`).

### 🌐 Cloud Mode (Fallback)

- When a user visits the live web link, the app dynamically detects the Linux cloud environment.  
- It gracefully disables the interactive Pygame simulator to prevent crashes.  
- Instead, it serves a pre-recorded GIF (`human_gameplay.gif`) demonstrating the extreme difficulty of manual human flight, alongside the AI metrics.

### 💻 Local Mode (Interactive)

- When a user clones the repository and runs it on their local machine (Windows/Mac), the app unlocks the **"Launch Simulator"** module.  
- It utilizes Python's `subprocess` library to spawn an isolated, independent Pygame window, allowing the user to play the game in real-time without freezing or blocking the Streamlit UI.


---

## 🚀 How to Run Locally

To fully experience the interactive Human vs. AI Simulator (which is safely disabled on the cloud to prevent headless server crashes), you need to run this project on your local machine.

### 📌 Prerequisites

- Python 3.8+ installed on your system  
- Git installed  

### 🧩 Step-by-Step Installation

#### 1. Clone the repository

```bash
git clone https://github.com/syedimad-ds/Game-Agent.git
cd Game-Agent
```

### 2. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit Dashboard

```bash
streamlit run app.py
    (or)
python -m streamlit run app.py
```

## 🎮 Play the Simulator

- Open the provided localhost link in your browser.  
- Since the application will successfully detect your local OS environment, the **"Launch Flight Simulator"** button will be unlocked.  
- Click it to safely spawn the Pygame window and attempt the landing yourself!  


---

## 📊 Project Highlights

This project demonstrates practical experience in Reinforcement Learning and building reliable, user-friendly applications.

### 🧠 AI & Machine Learning

- **Reinforcement Learning (RL):**  
  Implemented Deep Q-Networks (DQN) to solve a continuous state-space physics environment.  

- **Model Iteration:**  
  Tracked training progress from a random baseline to a refined model with stable and efficient landings.  

- **Environment Handling:**  
  Used OpenAI/Farama Gymnasium for state representation, reward design, and action management.  


### 💻 Software & Deployment

- **Adaptive Architecture:**  
  Designed the system to adjust behavior based on the deployment environment (cloud vs. local) to ensure stability.  

- **Process Management:**  
  Isolated the Pygame simulator from the Streamlit app to maintain responsiveness.  

- **Interface Design:**  
  Built a clean and intuitive dashboard to present model performance and interactions clearly.  

---

## 👨‍💻 Author

**Syed Imad Muzaffar**  
🎓 B.E. in Artificial Intelligence and Data Science
