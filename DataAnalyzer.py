import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import ast
import csv

class GameDataVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Game Data Visualizer")

        # Button to load file
        self.load_button = tk.Button(master, text="Load CSV File", command=self.load_file)
        self.load_button.pack(pady=10)

        # Text box to show stats
        self.text_box = tk.Text(master, height=20, width=80)
        self.text_box.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        df = pd.read_csv(file_path)

        # Convert stringified dicts to real dicts
        df['units_deployed'] = df['units_deployed'].apply(ast.literal_eval)
        df['damage_to_units'] = df['damage_to_units'].apply(ast.literal_eval)
        df['damage_to_towers'] = df['damage_to_towers'].apply(ast.literal_eval)
        df['resources_used'] = df['resources_used'].apply(ast.literal_eval)

        # Expand nested dicts into separate rows
        units_df = pd.json_normalize(df['units_deployed'])
        damage_units_df = pd.json_normalize(df['damage_to_units'])
        damage_towers_df = pd.json_normalize(df['damage_to_towers'])
        resources_df = pd.json_normalize(df['resources_used'])

        # Summarize totals
        total_units = units_df.sum()
        total_damage_units = damage_units_df.sum()
        total_damage_towers = damage_towers_df.sum()
        total_resources = resources_df.sum()

        summary = f"Total Units Deployed:\n{total_units}\n\n" \
                  f"Total Damage to Units:\n{total_damage_units}\n\n" \
                  f"Total Damage to Towers:\n{total_damage_towers}\n\n" \
                  f"Total Resources Used:\n{total_resources}\n"

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, summary)

        # Combine levels and outcomes for EDA
        outcome_counts = df.groupby(['level', 'outcome']).size().unstack(fill_value=0)

        # Plot Seaborn charts
        sns.set(style="whitegrid")

        # Units deployed barplot
        plt.figure(figsize=(10, 6))
        total_units.sort_values(ascending=False).plot(kind='bar')
        plt.title("Total Units Deployed")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig("total_units_deployed.png")
        plt.close()

        # Damage to units barplot
        plt.figure(figsize=(10, 6))
        total_damage_units.sort_values(ascending=False).plot(kind='bar', color='salmon')
        plt.title("Total Damage to Units")
        plt.ylabel("Damage")
        plt.tight_layout()
        plt.savefig("total_damage_units.png")
        plt.close()

        # Damage to towers barplot
        plt.figure(figsize=(10, 6))
        total_damage_towers.sort_values(ascending=False).plot(kind='bar', color='orange')
        plt.title("Total Damage to Towers")
        plt.ylabel("Damage")
        plt.tight_layout()
        plt.savefig("total_damage_towers.png")
        plt.close()

        # Resources used barplot
        plt.figure(figsize=(10, 6))
        total_resources.sort_values(ascending=False).plot(kind='bar', color='purple')
        plt.title("Total Resources Used")
        plt.ylabel("Amount")
        plt.tight_layout()
        plt.savefig("total_resources_used.png")
        plt.close()

        # Win/Loss ratio heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(outcome_counts, annot=True, fmt='d', cmap='Blues')
        plt.title("Win/Loss Count by Level")
        plt.tight_layout()
        plt.savefig("win_loss_heatmap.png")
        plt.close()

        self.text_box.insert(tk.END, "\nCharts saved as PNG files.")

# Run the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = GameDataVisualizer(root)
    root.mainloop()
