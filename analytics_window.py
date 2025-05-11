# analytics_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set backend before pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import ast
from collections import Counter
from PIL import Image, ImageTk
import os

class AnalyticsDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Analytics Dashboard")
        self.root.geometry("1400x900")

        # Set custom theme colors
        self.bg_color = "#2E3440"
        self.text_color = "#ECEFF4"
        self.accent_color = "#88C0D0"
        self.win_color = "#A3BE8C"
        self.loss_color = "#BF616A"

        # Configure root window
        self.root.configure(bg=self.bg_color)

        # Load background image
        try:
            self.bg_image = Image.open("background.jpg") if os.path.exists("background.jpg") else None
            if self.bg_image:
                self.bg_image = self.bg_image.resize((1400, 900), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(self.bg_image)
                self.bg_label = tk.Label(root, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Couldn't load background image: {e}")

        # Initialize data
        self.df = None
        self.current_level = "All"
        self.level_options = ["All"]

        # Create main container
        self.main_frame = ttk.Frame(root, style='Custom.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configure styles
        self.configure_styles()

        # Control panel
        self.control_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Level selection
        ttk.Label(self.control_frame, text="Select Level:", style='Custom.TLabel').pack(side=tk.LEFT, padx=5)
        self.level_var = tk.StringVar(value="All")
        self.level_menu = ttk.OptionMenu(
            self.control_frame, self.level_var, "All", *self.level_options,
            command=self.update_visualizations, style='Custom.TMenubutton'
        )
        self.level_menu.pack(side=tk.LEFT, padx=5)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_tabs()

        # Load data
        self.load_data()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Custom style configurations
        style.configure('Custom.TFrame', background=self.bg_color)
        style.configure('Custom.TLabel',
                        background=self.bg_color,
                        foreground=self.text_color,
                        font=('Arial', 10, 'bold'))
        style.configure('Custom.TMenubutton',
                        background=self.accent_color,
                        foreground=self.bg_color,
                        font=('Arial', 10))
        style.configure('Custom.TNotebook',
                        background=self.bg_color,
                        borderwidth=0)
        style.configure('Custom.TNotebook.Tab',
                        background="#4C566A",
                        foreground=self.text_color,
                        padding=[10, 5],
                        font=('Arial', 10, 'bold'))
        style.map('Custom.TNotebook.Tab',
                  background=[('selected', self.accent_color)],
                  foreground=[('selected', self.bg_color)])

    def create_tabs(self):
        # Tab 1: Overview
        self.overview_tab = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(self.overview_tab, text="Overview")

        # Tab 2: Unit Analysis
        self.unit_tab = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(self.unit_tab, text="Unit Analysis")

        # Tab 3: Resource Analysis
        self.resource_tab = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(self.resource_tab, text="Resource Analysis")

        # Tab 4: Performance Metrics
        self.metrics_tab = ttk.Frame(self.notebook, style='Custom.TFrame')
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
                self.level_menu['menu'].add_command(
                    label=option,
                    command=tk._setit(self.level_var, option, self.update_visualizations)
                )

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

        # Update visualizations with custom styles
        self.create_overview_tab(filtered_df)
        self.create_unit_tab(filtered_df)
        self.create_resource_tab(filtered_df)
        self.create_metrics_tab(filtered_df)

    def create_overview_tab(self, df):
        # Close any existing figures to prevent memory leaks
        plt.close('all')

        # Set custom color palette
        custom_palette = [self.win_color, self.loss_color]

        # Win/Loss Ratio
        fig1 = plt.figure(figsize=(12, 5), facecolor=self.bg_color)
        ax1 = fig1.add_subplot(121, facecolor=self.bg_color)

        win_counts = df['outcome'].value_counts()
        sns.barplot(
            x=win_counts.index,
            y=win_counts.values,
            ax=ax1,
            palette=custom_palette,
            hue=win_counts.index if len(win_counts) > 1 else None,
            legend=False
        )
        ax1.set_title("Win/Loss Ratio", color=self.text_color)
        ax1.set_ylabel("Count", color=self.text_color)
        ax1.set_xlabel("")
        ax1.tick_params(colors=self.text_color)
        ax1.spines['bottom'].set_color(self.text_color)
        ax1.spines['left'].set_color(self.text_color)

        # Duration Statistics
        ax2 = fig1.add_subplot(122, facecolor=self.bg_color)
        if not df.empty:
            sns.boxplot(
                x='outcome',
                y='duration',
                data=df,
                ax=ax2,
                palette=custom_palette,
                width=0.5,
                hue='outcome' if len(df['outcome'].unique()) > 1 else None,
                legend=False
            )
        ax2.set_title("Duration by Outcome", color=self.text_color)
        ax2.set_ylabel("Seconds", color=self.text_color)
        ax2.set_xlabel("")
        ax2.tick_params(colors=self.text_color)
        ax2.spines['bottom'].set_color(self.text_color)
        ax2.spines['left'].set_color(self.text_color)

        # Adjust layout and colors
        fig1.subplots_adjust(wspace=0.3)
        for text in fig1.texts:
            text.set_color(self.text_color)

        canvas1 = FigureCanvasTkAgg(fig1, master=self.overview_tab)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Custom toolbar
        toolbar1 = NavigationToolbar2Tk(canvas1, self.overview_tab)
        toolbar1.update()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_unit_tab(self, df):
        # Close any existing figures
        plt.close('all')

        # Set custom color palette based on number of unique units
        unique_units = set()
        for units in df['units_deployed']:
            unique_units.update(units.keys())
        num_units = len(unique_units)
        custom_palette = sns.color_palette("husl", num_units if num_units > 8 else 8)

        fig2 = plt.figure(figsize=(12, 8), facecolor=self.bg_color)

        # Unit counts
        ax1 = fig2.add_subplot(221, facecolor=self.bg_color)
        unit_list = []
        for units in df['units_deployed']:
            unit_list.append(pd.DataFrame.from_dict(units, orient='index').T)
        if unit_list:
            unit_counts = pd.concat(unit_list).sum()
            unit_counts = unit_counts.sort_values(ascending=False)

            sns.barplot(
                x=unit_counts.index,
                y=unit_counts.values,
                ax=ax1,
                palette=custom_palette,
                hue=unit_counts.index if len(unit_counts) > 1 else None,
                legend=False
            )
        ax1.set_title("Total Units Deployed", color=self.text_color)
        ax1.set_ylabel("Count", color=self.text_color)
        ax1.set_xlabel("")
        ax1.tick_params(axis='x', labelrotation=45)
        ax1.tick_params(colors=self.text_color)
        ax1.spines['bottom'].set_color(self.text_color)
        ax1.spines['left'].set_color(self.text_color)

        # Damage to Units
        ax2 = fig2.add_subplot(222, facecolor=self.bg_color)
        damage_list = []
        for damage in df['damage_to_units']:
            damage_list.append(pd.DataFrame.from_dict(damage, orient='index').T)
        if damage_list:
            damage_df = pd.concat(damage_list)
            damage_df.index = df['timestamp']

            damage_means = damage_df.mean().sort_values(ascending=False)
            damage_means.plot(
                kind='bar',
                ax=ax2,
                color=custom_palette[2]
            )
        ax2.set_title("Average Damage Dealt by Unit", color=self.text_color)
        ax2.set_ylabel("Damage", color=self.text_color)
        ax2.set_xlabel("")
        ax2.tick_params(axis='x', labelrotation=45)
        ax2.tick_params(colors=self.text_color)
        ax2.spines['bottom'].set_color(self.text_color)
        ax2.spines['left'].set_color(self.text_color)

        # Winrate by Unit
        ax3 = fig2.add_subplot(212, facecolor=self.bg_color)
        if not df.empty:
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
            sns.barplot(
                x=winrate_series.index,
                y=winrate_series.values,
                ax=ax3,
                palette=custom_palette,
                hue=winrate_series.index if len(winrate_series) > 1 else None,
                legend=False
            )
        ax3.set_title("Win Rate by Unit", color=self.text_color)
        ax3.set_ylabel("Win Rate", color=self.text_color)
        ax3.set_xlabel("")
        ax3.tick_params(axis='x', labelrotation=45)
        ax3.tick_params(colors=self.text_color)
        ax3.spines['bottom'].set_color(self.text_color)
        ax3.spines['left'].set_color(self.text_color)

        # Adjust layout and colors
        fig2.tight_layout()
        for text in fig2.texts:
            text.set_color(self.text_color)

        canvas2 = FigureCanvasTkAgg(fig2, master=self.unit_tab)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas2, self.unit_tab)
        toolbar2.update()

    def create_resource_tab(self, df):
        # Close any existing figures
        plt.close('all')

        # Set custom color palette
        custom_palette = sns.color_palette("Set2")

        fig3 = plt.figure(figsize=(12, 6), facecolor=self.bg_color)

        # Resource Usage Pie Chart
        ax1 = fig3.add_subplot(121, facecolor=self.bg_color)
        resource_list = []
        for resources in df['resources_used']:
            resource_list.append(pd.DataFrame([resources]))
        if resource_list:
            resource_sums = pd.concat(resource_list).sum()

            # Explode the largest wedge
            explode = [0.1 if i == resource_sums.idxmax() else 0 for i in resource_sums.index]

            wedges, texts, autotexts = ax1.pie(
                resource_sums,
                labels=resource_sums.index,
                autopct='%1.1f%%',
                startangle=140,
                colors=custom_palette,
                explode=explode,
                shadow=True,
                textprops={'color': self.text_color}
            )
        ax1.set_title("Resource Usage Distribution", color=self.text_color)

        # Resource Usage by Outcome
        ax2 = fig3.add_subplot(122, facecolor=self.bg_color)
        resource_data = []
        for _, row in df.iterrows():
            for resource, amount in row['resources_used'].items():
                resource_data.append({
                    'resource': resource,
                    'amount': amount,
                    'outcome': row['outcome']
                })
        if resource_data:
            resource_usage = pd.DataFrame(resource_data)

            sns.boxplot(
                x='resource',
                y='amount',
                hue='outcome',
                data=resource_usage,
                ax=ax2,
                palette=[self.win_color, self.loss_color],
                width=0.6
            )
        ax2.set_title("Resource Usage by Outcome", color=self.text_color)
        ax2.set_ylabel("Amount", color=self.text_color)
        ax2.set_xlabel("")
        ax2.tick_params(axis='x', labelrotation=45)
        ax2.tick_params(colors=self.text_color)
        ax2.spines['bottom'].set_color(self.text_color)
        ax2.spines['left'].set_color(self.text_color)
        if not df.empty and len(df['outcome'].unique()) > 1:
            ax2.legend(title='Outcome', title_fontsize='small', fontsize='x-small')
        else:
            ax2.legend().set_visible(False)

        # Adjust layout and colors
        fig3.tight_layout()
        for text in fig3.texts:
            text.set_color(self.text_color)

        canvas3 = FigureCanvasTkAgg(fig3, master=self.resource_tab)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar3 = NavigationToolbar2Tk(canvas3, self.resource_tab)
        toolbar3.update()

    def create_metrics_tab(self, df):
        # Close any existing figures
        plt.close('all')

        # Set custom color palette
        custom_palette = sns.color_palette("Paired")

        fig4 = plt.figure(figsize=(12, 10), facecolor=self.bg_color)

        # Damage vs Duration
        ax1 = fig4.add_subplot(211, facecolor=self.bg_color)
        damage_list = []
        for damage in df['damage_to_units']:
            damage_list.append(pd.DataFrame.from_dict(damage, orient='index').T)
        if damage_list:
            damage_df = pd.concat(damage_list)
            total_damage = damage_df.sum(axis=1)
            durations = df['duration']

            color1 = custom_palette[1]
            ax1.set_xlabel('Run Index', color=self.text_color)
            ax1.set_ylabel('Total Damage', color=color1)
            ax1.plot(
                total_damage.index,
                total_damage.values,
                color=color1,
                marker='o',
                markersize=6,
                linewidth=2,
                label='Total Damage'
            )
            ax1.tick_params(axis='y', labelcolor=color1)
            ax1.tick_params(axis='x', colors=self.text_color)
            ax1.spines['bottom'].set_color(self.text_color)
            ax1.spines['left'].set_color(color1)

            ax2 = ax1.twinx()
            color2 = custom_palette[3]
            ax2.set_ylabel('Duration (seconds)', color=color2)
            ax2.plot(
                total_damage.index,
                durations.values,
                color=color2,
                marker='s',
                linestyle='--',
                markersize=5,
                linewidth=2,
                label='Duration'
            )
            ax2.tick_params(axis='y', labelcolor=color2)
            ax2.spines['right'].set_color(color2)

            ax1.set_title('Total Damage vs. Duration per Run', color=self.text_color)
            fig4.legend(
                loc='upper right',
                bbox_to_anchor=(0.9, 0.9),
                frameon=False,
                labelcolor=self.text_color
            )

        # Correlation Heatmap
        ax3 = fig4.add_subplot(212, facecolor=self.bg_color)
        if not df.empty and len(damage_list) > 0:
            try:
                corr_df = pd.DataFrame({
                    'duration': df['duration'].values,
                    'total_damage': damage_df.sum(axis=1).values,
                    'win': df['outcome'].apply(lambda x: 1 if x == 'win' else 0).values
                })
                sns.heatmap(
                    corr_df.corr(),
                    annot=True,
                    cmap='coolwarm',
                    ax=ax3,
                    cbar_kws={'label': 'Correlation'}
                )
            except Exception as e:
                print(f"Error creating correlation heatmap: {e}")
                ax3.text(0.5, 0.5, 'Not enough data for correlation',
                         ha='center', va='center', color=self.text_color)
        else:
            ax3.text(0.5, 0.5, 'Not enough data for correlation',
                     ha='center', va='center', color=self.text_color)

        ax3.set_title("Correlation Heatmap", color=self.text_color)
        ax3.tick_params(colors=self.text_color)

        # Adjust layout and colors
        fig4.tight_layout()
        for text in fig4.texts:
            text.set_color(self.text_color)

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

    # Set matplotlib backend before creating any figures
    matplotlib.use('TkAgg')

    open_window()