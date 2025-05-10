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

7. To run the jupyther notebook:
    ```bash
     jupyther notebook
    ```
8.pick file:
    ```
    choose graphs/level1 - graphs/level6
    ```
---

The project includes a Jupyter Notebook (`level1.ipynb` ) till (`level6.ipynb`)that generates the following charts from the recorded battle statistics:

1. **Units Deployed** → Bar Chart  
   Compare the frequency of unit deployment across all battles.

2. **Damage Dealt** → Stacked Bar Chart  
   Show total damage to units and towers, stacked per unit type.

3. **Battle Duration** → Histogram  
   Display the distribution of battle durations.

4. **Player Resource Usage** → Pie Chart  
   Visualize the percentage use of Solar, Lunar, and Eclipse resources.

5. **Win/Loss Ratio** → Pie Chart  
   Show overall player success rate.






jupyter notebook visualization.ipynb
## Project Screenshots

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
[YouTube Presentation Link](https://www.youtube.com/watch?v=YOUR_VIDEO_LINK)
