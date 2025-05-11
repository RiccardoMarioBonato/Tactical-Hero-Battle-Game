# Tactical Hero Battle Game

This project is a 2D side-scrolling tactical battle game where players must defend their base by strategically deploying hero units to stop waves of enemies.  
The game features a variety of hero classes, enemy types, levels, and resource management mechanics to create an engaging strategy experience.

---

## Game Concept

Players defend their base by deploying heroes using three types of resources: Solar, Lunar, and Eclipse.  
Heroes have unique abilities, stats, and costs.  
Enemies spawn in waves, increasing in difficulty over time.  
Players earn progression by completing levels, unlocking new heroes, and advancing to more challenging stages.  
The game ends when either the player or the enemy base is destroyed, and detailed battle statistics are recorded.

---

## Python Version

Requires **Python >= 3.10**

---

## Current Features

- Multiple hero classes with unique abilities and resource costs  
- Enemy types with varying behaviors and strengths  
- Level system with six progressively harder levels  
- Real-time resource management (Solar, Lunar, Eclipse)  
- Hero selection and unlock system  
- Battle statistics tracking:
  - Units deployed  
  - Damage dealt to units and towers  
  - Battle duration  
  - Resource usage  
  - Win/loss outcome  
- Data saved to CSV for later visualization

---

## How to Run the Application

1. Clone the repository
    ```bash
    git clone https://github.com/RiccardoMarioBonato/Tactical-Hero-Battle-Game.git
    ```

2. Change into the project directory
    ```bash
    cd Tactical-Hero-Battle-Game
    ```

3. Create a virtual environment
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment

    MacOS or Linux:
    ```bash
    source venv/bin/activate
    ```

    Windows:
    ```bash
    venv\Scripts\activate
    ```

5. Install the required packages
    ```bash
    pip install -r requirements.txt
    ```

6. Run the application
    ```bash
    python main.py
    ```

7. View analytics dashboard (after battles) without the game engine for weaker rigs:
    ```bash
     python analytics_window.py
    ```
---

## 📊 Data Visualization

Recorded battle stats are saved in `game_stats.csv`. You can view them with:

- 📈 `analytics_window.py` — GUI-based dashboard for full analytics

### 🔑 Key Graphs

| **Graph**                    | **Description**                                                   |
|-----------------------------|-------------------------------------------------------------------|
| **Win/Loss Ratio**          | Bar Chart comparing number of wins and losses                     |
| **Battle Duration**         | Boxplot showing duration distribution across outcomes             |
| **Units Deployed**          | Bar Chart of total unit deployments                               |
| **Unit Damage Output**      | Bar Chart showing average damage dealt by each unit               |
| **Unit Win Rate**           | Bar Chart comparing how often each unit contributed to a victory  |
| **Resource Usage**          | Pie Chart of Solar, Lunar, and Eclipse usage + outcome breakdown  |
| **Total Damage vs Duration**| Dual Line Chart comparing total damage with battle duration       |
| **Correlation Heatmap**     | Correlation matrix for duration, damage, and win outcome          |





Gameplay screenshots:
- Available in `/screenshots/gameplay/`

Visualization screenshots:
- Available in `/screenshots/visualization/`

---

## License

This project uses the [MIT License](LICENSE).

---

## YouTube Presentation

Watch the 5-minute project presentation video:  
[YouTube Presentation Link](https://www.youtube.com/watch?v=_GoVpilOQjs)
