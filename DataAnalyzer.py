import csv
import ast
from collections import defaultdict
import matplotlib.pyplot as plt


class DataAnalyzer:
    def __init__(self, filename="game_stats.csv"):
        self.filename = filename

    def load_data(self):
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def generate_reports(self):
        data = self.load_data()

        # Unit Deployment Analysis
        unit_counts = defaultdict(int)
        for row in data:
            units = ast.literal_eval(row['units_deployed'])
            for unit, count in units.items():
                unit_counts[unit] += count

        # Damage Analysis
        damage_by_unit = defaultdict(int)
        for row in data:
            damage = ast.literal_eval(row['damage_dealt'])
            for unit, amount in damage.items():
                damage_by_unit[unit] += amount

        # Win/Loss by Level
        level_outcomes = defaultdict(lambda: {'wins': 0, 'losses': 0})
        for row in data:
            level = row['level']
            if row['outcome'] == 'win':
                level_outcomes[level]['wins'] += 1
            else:
                level_outcomes[level]['losses'] += 1

        # Generate visualizations
        self._create_bar_chart(unit_counts, "Units Deployed", "Unit Type", "Count")
        self._create_bar_chart(damage_by_unit, "Damage Dealt", "Unit Type", "Damage")
        self._create_win_loss_chart(level_outcomes)

    def _create_bar_chart(self, data, title, xlabel, ylabel):
        plt.figure(figsize=(10, 6))
        plt.bar(data.keys(), data.values())
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{title.replace(' ', '_')}.png")
        plt.close()

    def _create_win_loss_chart(self, data):
        levels = sorted(data.keys())
        wins = [data[level]['wins'] for level in levels]
        losses = [data[level]['losses'] for level in levels]

        plt.figure(figsize=(10, 6))
        plt.bar(levels, wins, label='Wins')
        plt.bar(levels, losses, bottom=wins, label='Losses')
        plt.title("Win/Loss Ratio by Level")
        plt.xlabel("Level")
        plt.ylabel("Count")
        plt.legend()
        plt.tight_layout()
        plt.savefig("Win_Loss_Ratio.png")
        plt.close()