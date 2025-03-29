import tkinter as tk
from tkinter import ttk, font
from typing import Dict, Callable
from constants import THEMES, AVAILABLE_EMOJIS

class GameMenu:
    def __init__(self, parent, callbacks: Dict[str, Callable]):
        """Initialisiert das Spielmenü mit Einstellungsoptionen"""
        self.parent = parent
        self.callbacks = callbacks  # Funktionsreferenzen für verschiedene Aktionen
        
        # Oberer Bereich: Titel
        title_font = font.Font(family='Helvetica', size=18, weight='bold')
        title_label = ttk.Label(parent, text="🎮 Tic Tac Toe Deluxe 🎮", font=title_font)
        title_label.pack(pady=(0, 15))
        
        # Options-Frame
        self.options_frame = ttk.Frame(parent)
        self.options_frame.pack(fill=tk.X, pady=10)
        
        # Emoji-Auswahl
        emoji_frame = ttk.LabelFrame(self.options_frame, text="Dein Emoji")
        emoji_frame.pack(side=tk.LEFT, padx=5)
        
        self.emoji_var = tk.StringVar()
        self.emoji_menu = ttk.Combobox(emoji_frame, textvariable=self.emoji_var, width=5, 
                                     font=('Arial', 14))
        self.emoji_menu['values'] = AVAILABLE_EMOJIS['Tiere']
        self.emoji_menu.current(0)
        self.emoji_menu.pack(padx=10, pady=5)
        self.emoji_menu.bind("<<ComboboxSelected>>", 
                           lambda event: self.callbacks['update_emoji'](self.emoji_var.get()))
        
        # Emoji-Kategorie auswählen
        emoji_cat_frame = ttk.LabelFrame(self.options_frame, text="Emoji-Kategorie")
        emoji_cat_frame.pack(side=tk.LEFT, padx=5)
        
        self.emoji_cat_var = tk.StringVar(value='Tiere')
        emoji_cats = list(AVAILABLE_EMOJIS.keys())
        emoji_cat_menu = ttk.Combobox(emoji_cat_frame, textvariable=self.emoji_cat_var, 
                                    values=emoji_cats, width=10)
        emoji_cat_menu.pack(padx=10, pady=5)
        emoji_cat_menu.bind("<<ComboboxSelected>>", 
                          lambda event: self.callbacks['update_emoji_category'](self.emoji_cat_var.get()))
        
        # Thema auswählen
        theme_frame = ttk.LabelFrame(self.options_frame, text="Thema")
        theme_frame.pack(side=tk.LEFT, padx=5)
        
        self.theme_var = tk.StringVar(value='Hell')
        theme_menu = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                values=list(THEMES.keys()), width=8)
        theme_menu.pack(padx=10, pady=5)
        theme_menu.bind("<<ComboboxSelected>>", 
                      lambda event: self.callbacks['update_theme'](self.theme_var.get()))
        
        # Schwierigkeitsgrad
        diff_frame = ttk.LabelFrame(self.options_frame, text="Schwierigkeit")
        diff_frame.pack(side=tk.LEFT, padx=5)
        
        self.diff_var = tk.StringVar(value='Mittel')
        diff_menu = ttk.Combobox(diff_frame, textvariable=self.diff_var, 
                               values=['Leicht', 'Mittel', 'Schwer'], width=8)
        diff_menu.pack(padx=10, pady=5)
        diff_menu.bind("<<ComboboxSelected>>", 
                     lambda event: self.callbacks['update_difficulty'](self.diff_var.get()))
        
        # Neues Spiel Button
        new_game_btn = ttk.Button(self.options_frame, text="Neues Spiel", 
                                command=self.callbacks['new_game'])
        new_game_btn.pack(side=tk.RIGHT, padx=10)
        
        # Status- und Informationsbereich
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="Bereit zum Spielen! Drücke 'Neues Spiel'")
        status_label = ttk.Label(info_frame, textvariable=self.status_var, font=('Arial', 12))
        status_label.pack(pady=5)
    
    def update_status(self, message: str) -> None:
        """Aktualisiert die Statusanzeige"""
        self.status_var.set(message)
    
    def update_emoji_list(self, category: str) -> None:
        """Aktualisiert die Emoji-Liste basierend auf der gewählten Kategorie"""
        self.emoji_menu['values'] = AVAILABLE_EMOJIS[category]
        self.emoji_menu.current(0)
