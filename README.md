# ⚡ HackTeamMatcher Pro

> **The smartest way to build your dream squad.** > Stop randomly DMing people. Use AI to find the perfect teammate with matching skills and availability in seconds.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-ff4b4b)
![Scikit-Learn](https://img.shields.io/badge/AI-Scikit--Learn-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 🏆 Project Category
**Category 6: Community & Collaboration Tools** *Also enables: Category 1 (Helping AI Agents) & Category 4 (Web Dev)*

---

## 📖 The Problem
Hackathons are short. Finding a team is hard.
Most students spend the first 6 hours of a hackathon spamming Discord channels with *"Hi, I know Python, anyone need a member?"*

It's chaotic, inefficient, and often leads to unbalanced teams (e.g., 4 backend devs and 0 designers).

## 🚀 The Solution
**HackTeamMatcher Pro** uses vector mathematics (K-Nearest Neighbors Algorithm) to calculate compatibility scores between hackers. It doesn't just match based on a text search; it matches based on:
1.  **Skill Complements:** Finding people who fill your gaps.
2.  **Availability:** Matching "Hardcore" (40hrs) with "Hardcore", and "Casual" with "Casual".
3.  **Role Logic:** Ensuring a team has the right mix of Builders, Designers, and Data Scientists.

---

## ✨ Key Features

### 🧠 AI-Powered Matching (KNN)
We treat every user as a vector in a multi-dimensional space (Python, Frontend, Backend, Design, SQL, Availability). The app calculates the **Euclidean Distance** between you and other candidates to find your mathematical neighbors.


### ⚠️ Immersive UI & "Hazard Mode"
A modern, dark-themed "Glassmorphism" UI designed for gamers and hackers. Includes a live **Simulation Mode** warning banner (CSS Hazard Tape) to indicate the demo environment.

### 🛡️ Live Squad Management
* **Register a Team:** Create a squad, set requirements (Hours/Role), and appear in the "Join" feed.
* **Self-Discovery:** Search for yourself to see how your profile appears to others (Gold Highlighted).
* **Real-time Updates:** Changing your sliders updates the database instantly for the current session.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python)
* **Styling:** Custom CSS (Glassmorphism, Animations, Flexbox)
* **Machine Learning:** Scikit-Learn (`NearestNeighbors`)
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly (Radar Charts/Spider Graphs)


---

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/HackTeamMatcher-Pro.git](https://github.com/YOUR_USERNAME/HackTeamMatcher-Pro.git)
    cd HackTeamMatcher-Pro
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Generate Simulation Data**
    *(Creates a dummy database of 500+ students)*
    ```bash
    python generate_data.py
    ```

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```

---

## 🔮 Future Roadmap

* **Discord Bot Integration:** Directly DM matched users via bot.
* **GitHub Scraping:** verify skills by analyzing a user's actual code contributions.
* **Team Balancing Algorithm:** An algorithm that suggests the *perfect* 4th member for an existing trio.

---

## 🤝 Contributing

This project was built for the **Hybrid Builder Challenge**.
Developed by **Hitarth Patel**.
