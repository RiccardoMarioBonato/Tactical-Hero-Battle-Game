# Tactical Hero Battle Game

## 🎮 Project Overview
**Tactical Hero Battle Game** is a 2D side-scrolling tactical strategy game inspired by *Line Rangers* and *Battle Cats*.  
Players deploy unique hero units onto the battlefield to **defend their base** and **destroy the enemy base**.  
The game features **real-time resource management**, **hero and enemy classes**, **wave-based combat**, and a **level progression system**.

---

## 🧠 Game Concept

- **🎯 Objective**: Win by destroying the enemy's base while protecting your own.
- **⚙️ Core Mechanics**:
  - Deploy heroes using **Solar**, **Lunar**, and **Eclipse** resources.
  - Each unit has unique **stats, abilities, and resource costs**.
  - Enemies spawn in escalating waves as difficulty increases.
  - **Levels and heroes unlock progressively**.
- **📊 Data Component**:
  - Tracks detailed battle statistics:
    - Units deployed
    - Damage to units and towers
    - Resource usage
    - Battle duration
    - Win/Loss outcome
  - All stats are saved to `game_stats.csv` for visualization and analysis.

---

## 🖥️ Installation & Running Instructions

1. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the game:
    ```bash
    python main.py
    ```

---

## 🧱 Required Packages

The project requires the following Python libraries (listed in `requirements.txt`):

- `pygame`  
- `pandas`  
- `seaborn`  
- `matplotlib`  
- `Pillow`

---

## 🧩 UML Class Diagram

Below is the UML diagram illustrating key classes, patterns, and relationships:

![UML Diagram](file%20related/UML_updated.JPG)

---

## ✨ Game Features

- ✅ Multiple hero & enemy classes with inheritance-based stats and logic  
- ✅ Wave-based enemy AI scaling with level progression  
- ✅ Tower health, unit combat, and projectile systems  
- ✅ Hero selection screen with team size restriction  
- ✅ Level selection system with lock/unlock logic  
- ✅ Real-time resource management (solar, lunar, eclipse)  
- ✅ Auto-play and simulation mode for automated data generation  
- ✅ Detailed logging to `game_stats.csv` for data analytics

---

## 📊 Data Collected

| **Metric**              | **Description**                                |
|-------------------------|------------------------------------------------|
| Units Deployed          | Per hero type and total per battle             |
| Damage to Units/Towers  | Per unit type and overall                      |
| Battle Duration         | Measures difficulty and player efficiency      |
| Resource Usage          | Solar, Lunar, and Eclipse usage per battle     |
| Win/Loss Outcome        | Overall player performance and strategies      |

---

## 📈 Visualization Plan

Data can be viewed in two formats:

- `analytics_window.py` – an interactive Tkinter dashboard with 4 analysis tabs  
- `level1.ipynb` to `level6.ipynb` – Jupyter Notebooks for level-specific analysis  

**Key Graphs:**

- 🟦 Win/Loss Ratio → Bar Chart  
- ⏱️ Battle Duration → Boxplot  
- 🧍 Units Deployed → Bar Chart  
- 💥 Unit Damage Output → Bar Chart  
- 🏆 Unit Win Rate → Bar Chart  
- 🔄 Resource Usage → Pie Chart + Outcome Comparison  
- 📊 Total Damage vs Duration → Dual Axis Line Chart  
- 🔥 Correlation Heatmap → Relation between Duration, Winrate, and Damage  

---

## 🚀 Project Status

| **Progress** | **Milestone**                  |
|--------------|-------------------------------|
| ✅ 50%        | Core mechanics, unit logic     |
| ✅ 75%        | Data collection, analytics     |
| ✅ 100%       | Final visuals & submission     |

---

## 🏷️ GitHub Tags

- `v0.5` → 50% project checkpoint  
- `v1.0` → 100% submission (before balancing)  
- `v1.5` → 100% submission with unit balancing and optimization  

---

## 📺 YouTube Presentation

🎥 [Watch the project presentation on YouTube](https://www.youtube.com/watch?v=_GoVpilOQjs)

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).
