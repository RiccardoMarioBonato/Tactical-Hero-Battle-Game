# Tactical Hero Battle Game

## Project Overview
The **Tactical Hero Battle Game** is a 2D side-scrolling strategy game inspired by *Line Ranger* and *Battle Cats*.  
Players deploy unique hero units onto the battlefield to defend their base and destroy the enemy’s base.  
The game features real-time resource management, wave-based enemy spawns, hero selection, and progressive difficulty.

## Concept
- **Objective**: Destroy the opponent’s base while defending your own.
- **Mechanics**:
  - Deploy heroes using three types of resources: Solar, Lunar, and Eclipse.
  - Each hero has unique costs, stats, and abilities.
  - Enemies spawn in waves and increase in difficulty over time.
  - Completing levels unlocks new levels and heroes.
- **Data Component**:
  - Tracks battle statistics such as units deployed, damage dealt, battle duration, resources used, and win/loss outcome.
  - Stores data in CSV format for later visualization.

## Installation and Running Instructions
1. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the main game:
    ```bash
    python main.py
    ```

## Required Packages
All required packages are listed in `requirements.txt`.

## UML Class Diagram
file related\UML.JPG

## Game Features
✅ Hero and enemy classes with unique stats and abilities  
✅ Resource system with Solar, Lunar, and Eclipse energy  
✅ Tower health, unit movement, and collision-based combat  
✅ Level selection with unlockable levels  
✅ Hero selection with maximum team size  
✅ CSV-based battle data logging  
✅ Asset loader to handle game images and sprites

## Data Collected
- Units Deployed (per type and total)
- Damage Dealt to Units and Towers
- Battle Duration
- Resource Usage
- Win/Loss Outcome

## Visualization Plans
The collected data will be visualized using:
- Bar charts (units deployed)
- Stacked bar or line charts (damage dealt)
- Pie charts (resource usage)
- Histograms (battle duration)
- Percentage gauges (win/loss ratio)

## Project Status
- Current progress: ~75% complete  
- Remaining work:
  - Add additional hero/enemy classes  
  - Add data visualization script (Python/Jupyter Notebook)  
  - Expand unit animations and visual effects

## GitHub Tags
- `v0.5` → 50% submission  
- `v1.0` → final 100% submission

## YouTube Presentation Video
[YouTube Presentation Link](https://www.youtube.com/watch?v=YOUR_VIDEO_LINK)

---

## License
This project is licensed under the [MIT License](LICENSE).
