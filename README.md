# 🔖 v0.5 – 50% Project Checkpoint

This version marks the halfway milestone of the **Tactical Hero Battle Game** project. It includes a **fully playable prototype** with the main gameplay mechanics functioning as intended.

---

## ✅ Features Completed

### 🎮 Playable Game Core
- Player and enemy towers with health, damage, and game-over logic
- Units can be deployed by the player and will automatically move, collide, and engage in combat
- Damage system implemented for both units and towers

### 👥 Unit System
- At least 5 distinct hero units implemented:
  - `LumberJack`, `Pantheon`, `BrownBeard`, `Kitsune`, `YamabushiTengu`
- Each unit has unique stats (HP, damage, speed, cost)
- Utilizes OOP inheritance from a shared `Unit` base class

### 🧠 Enemy AI
- Enemies spawn in waves with increasing difficulty
- Enemies can engage player units and damage the player's tower
- Includes bosses and regular enemy types

### 💰 Resource Management
- Real-time resource system with:
  - **Solar**, **Lunar**, and **Eclipse** resources
- Units consume appropriate resource combinations when deployed
- Resources regenerate over time and are displayed during gameplay

### 🧍 Unit Selection System
- Pre-match character selection is available
- Supports 3-character deployment per match
- Keyboard bindings (`C`, `V`, `B`) control deployed units from the selected team

### 🧱 Programming Architecture
- Modular design using Object-Oriented Programming principles
- Design patterns:
  - Singleton for `GameStats`, `Resources`, `UnitConfig`
  - Base-class inheritance for unit types

---

## ❌ Not Yet Implemented

### 📊 Data Visualization
- No analytical dashboard or graphs yet
- Although battle stats are logged in `game_stats.csv`, no visual reports are generated

### 🖼️ GUI Systems
- No level or hero selection GUI implemented yet
- No win/lose end screen or data review screen

### 📁 Documentation
- Screenshots not yet included in the `screenshots` folder
- UML diagram may be handled separately in the final version

---

## ⚙️ Installation & Running

To install and run the project:

```bash
pip install -r requirements.txt
python main.py
