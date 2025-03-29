import tkinter as tk
from tkinter import ttk
from utils.storage import GameStats

class StatsDisplay:
    def __init__(self, parent):
        """Initialisiert die Statistikanzeige"""
        # Statistikbereich
        self.stats_frame = ttk.LabelFrame(parent, text="Spielstatistiken")
        self.stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_vars = {
            'wins': tk.StringVar(value=f"Siege: 0"),
            'losses': tk.StringVar(value=f"Niederlagen: 0"),
            'ties': tk.StringVar(value=f"Unentschieden: 0"),
            'total': tk.StringVar(value=f"Gesamt: 0")
        }
        
        stats_inner = ttk.Frame(self.stats_frame)
        stats_inner.pack(fill=tk.X, pady=5)
        
        for i, (key, var) in enumerate(self.stats_vars.items()):
            lbl = ttk.Label(stats_inner, textvariable=var)
            lbl.grid(row=0, column=i, padx=20, pady=5)
    
    def update_stats(self, stats: GameStats) -> None:
        """Aktualisiert die Statistikanzeige"""
        self.stats_vars['wins'].set(f"Siege: {stats.wins}")
        self.stats_vars['losses'].set(f"Niederlagen: {stats.losses}")
        self.stats_vars['ties'].set(f"Unentschieden: {stats.ties}")
        self.stats_vars['total'].set(f"Gesamt: {stats.total_games}")
