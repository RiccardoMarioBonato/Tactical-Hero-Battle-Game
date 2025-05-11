# analytics_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import ast
from collections import Counter
from PIL import Image, ImageTk
import numpy as np


class AnalyticsDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Analytics Dashboard")
        self.root.geometry("1400x900")

        # Initialize data
        self.df = None
        self.current_level = "All"
        self.level_options = ["All"]

        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Control panel
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Level selection
        ttk.Label(self.control_frame, text="Select Level:").pack(side=tk.LEFT, padx=5)
        self.level_var = tk.StringVar(value="All")
        self.level_menu = ttk.OptionMenu(self.control_frame, self.level_var, "All",
                                         *self.level_options,
                                         command=self.update_visualizations)
        self.level_menu.pack(side=tk.LEFT, padx=5)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_tabs()

        # Load data
        self.load_data()

    def create_tabs(self):
        # Tab 1: Overview
        self.overview_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_tab, text="Overview")

        # Tab 2: Unit Analysis
        self.unit_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.unit_tab, text="Unit Analysis")

        # Tab 3: Resource Analysis
        self.resource_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.resource_tab, text="Resource Analysis")

        # Tab 4: Performance Metrics
        self.metrics_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.metrics_tab, text="Performance Metrics")

    def load_data(self):
        try:
            self.df = pd.read_csv("Graphs/game_stats.csv")

            # Convert string dictionaries to actual dictionaries
            for col in ['units_deployed', 'damage_to_units', 'damage_to_towers', 'resources_used']:
                self.df[col] = self.df[col].apply(ast.literal_eval)

            # Update level options
            levels = sorted(self.df['level'].unique())
            self.level_options.extend([f"Level {lvl}" for lvl in levels])
            self.level_menu['menu'].delete(0, 'end')
            for option in self.level_options:
                self.level_menu['menu'].add_command(label=option,
                                                    command=tk._setit(self.level_var, option,
                                                                      self.update_visualizations))

            # Initial visualizations
            self.update_visualizations()

        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find game_stats.csv file")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def get_filtered_data(self):
        if self.current_level == "All":
            return self.df.copy()
        else:
            level_num = int(self.current_level.split()[-1])
            return self.df[self.df['level'] == level_num].copy()

    def update_visualizations(self, *args):
        self.current_level = self.level_var.get()
        filtered_df = self.get_filtered_data()

        # Clear previous visualizations
        for tab in [self.overview_tab, self.unit_tab, self.resource_tab, self.metrics_tab]:
            for widget in tab.winfo_children():
                widget.destroy()

        # Update visualizations
        self.create_overview_tab(filtered_df)
        self.create_unit_tab(filtered_df)
        self.create_resource_tab(filtered_df)
        self.create_metrics_tab(filtered_df)

    def create_overview_tab(self, df):
        # Win/Loss Ratio
        fig1 = plt.figure(figsize=(12, 5))
        ax1 = fig1.add_subplot(121)
        win_counts = df['outcome'].value_counts()
        sns.barplot(x=win_counts.index, y=win_counts.values, ax=ax1)
        ax1.set_title("Win/Loss Ratio")
        ax1.set_ylabel("Count")

        # Duration Statistics
        ax2 = fig1.add_subplot(122)
        sns.boxplot(x='outcome', y='duration', data=df, ax=ax2)
        ax2.set_title("Duration by Outcome")
        ax2.set_ylabel("Seconds")

        canvas1 = FigureCanvasTkAgg(fig1, master=self.overview_tab)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add navigation toolbar
        toolbar1 = NavigationToolbar2Tk(canvas1, self.overview_tab)
        toolbar1.update()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_unit_tab(self, df):
        # Unit Deployment Analysis
        fig2 = plt.figure(figsize=(12, 8))

        # Unit counts
        ax1 = fig2.add_subplot(221)
        unit_counts = pd.DataFrame(df['units_deployed'].tolist()).sum()
        unit_counts.sort_values(ascending=False, inplace=True)
        sns.barplot(x=unit_counts.index, y=unit_counts.values, ax=ax1)
        ax1.set_title("Total Units Deployed")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')

        # Damage to Units
        ax2 = fig2.add_subplot(222)
        damage_df = pd.DataFrame(df['damage_to_units'].tolist())
        damage_df.index = df['timestamp']
        damage_df.mean().sort_values(ascending=False).plot(kind='bar', ax=ax2)
        ax2.set_title("Average Damage Dealt by Unit")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')

        # Winrate by Unit
        ax3 = fig2.add_subplot(212)
        win_df = df[df['outcome'] == 'win']
        win_counts = Counter()
        for d in win_df['units_deployed']:
            win_counts.update(d.keys())

        total_counts = Counter()
        for d in df['units_deployed']:
            total_counts.update(d.keys())

        winrates = {}
        for char in total_counts:
            wins = win_counts[char]
            total = total_counts[char]
            winrates[char] = wins / total if total > 0 else 0

        winrate_series = pd.Series(winrates).sort_values(ascending=False)
        sns.barplot(x=winrate_series.index, y=winrate_series.values, ax=ax3)
        ax3.set_title("Win Rate by Unit")
        ax3.set_ylabel("Win Rate")
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')

        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=self.unit_tab)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas2, self.unit_tab)
        toolbar2.update()

    def create_resource_tab(self, df):
        fig3 = plt.figure(figsize=(12, 6))

        # Resource Usage Pie Chart
        ax1 = fig3.add_subplot(121)
        resource_sums = pd.DataFrame(df['resources_used'].tolist()).sum()
        ax1.pie(resource_sums, labels=resource_sums.index, autopct='%1.1f%%', startangle=140)
        ax1.set_title("Resource Usage Distribution")

        # Resource Usage by Outcome
        ax2 = fig3.add_subplot(122)
        resource_usage = pd.DataFrame()
        for _, row in df.iterrows():
            for resource, amount in row['resources_used'].items():
                resource_usage = resource_usage.append({
                    'resource': resource,
                    'amount': amount,
                    'outcome': row['outcome']
                }, ignore_index=True)

        sns.boxplot(x='resource', y='amount', hue='outcome', data=resource_usage, ax=ax2)
        ax2.set_title("Resource Usage by Outcome")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')

        fig3.tight_layout()
        canvas3 = FigureCanvasTkAgg(fig3, master=self.resource_tab)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar3 = NavigationToolbar2Tk(canvas3, self.resource_tab)
        toolbar3.update()

    def create_metrics_tab(self, df):
        fig4 = plt.figure(figsize=(12, 10))

        # Damage vs Duration
        ax1 = fig4.add_subplot(211)
        damage_df = pd.DataFrame(df['damage_to_units'].tolist())
        total_damage = damage_df.sum(axis=1)
        durations = df['duration']

        color = 'tab:blue'
        ax1.set_xlabel('Run Index')
        ax1.set_ylabel('Total Damage', color=color)
        ax1.plot(total_damage.index, total_damage.values, color=color, marker='o',
                 label='Total Damage')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Duration (seconds)', color=color)
        ax2.plot(total_damage.index, durations.values, color=color, marker='s', linestyle='--',
                 label='Duration')
        ax2.tick_params(axis='y', labelcolor=color)

        ax1.set_title('Total Damage vs. Duration per Run')
        fig4.legend(loc='upper right')

        # Correlation Heatmap
        ax3 = fig4.add_subplot(212)
        corr_df = pd.DataFrame({
            'duration': df['duration'],
            'total_damage': damage_df.sum(axis=1),
            'win': df['outcome'].apply(lambda x: 1 if x == 'win' else 0)
        })
        sns.heatmap(corr_df.corr(), annot=True, cmap='coolwarm', ax=ax3)
        ax3.set_title("Correlation Heatmap")

        fig4.tight_layout()
        canvas4 = FigureCanvasTkAgg(fig4, master=self.metrics_tab)
        canvas4.draw()
        canvas4.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar4 = NavigationToolbar2Tk(canvas4, self.metrics_tab)
        toolbar4.update()


def open_window():
    try:
        root = tk.Tk()
        app = AnalyticsDashboard(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open analytics window: {str(e)}")


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
    open_window()