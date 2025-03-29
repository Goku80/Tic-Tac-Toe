import tkinter as tk
from typing import List, Callable, Optional
from constants import THEMES

class GameBoard:
    def __init__(self, parent, theme_name: str, on_move_callback: Callable[[int], None]):
        """Initialisiert das Spielbrett"""
        self.parent = parent
        self.theme_name = theme_name
        self.on_move_callback = on_move_callback
        
        # Spielbrett-Frame
        self.board_frame = tk.Frame(self.parent)
        self.board_frame.pack(padx=20, pady=20, expand=True)
        
        # Canvas für die Linien
        self.canvas = tk.Canvas(self.board_frame, width=320, height=320, 
                               bg=THEMES[self.theme_name]['bg'], highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=3, columnspan=3)
        
        # Spielfeldbuttons erstellen
        self.buttons = []
        btn_font = tk.font.Font(family='Arial', size=20)
        for i in range(9):
            row, col = i // 3, i % 3
            btn = tk.Button(self.board_frame, text='', font=btn_font, width=3, height=1,
                          command=lambda idx=i+1: self.on_move_callback(idx),
                          bg=THEMES[self.theme_name]['button_bg'],
                          activebackground=THEMES[self.theme_name]['button_active_bg'],
                          fg=THEMES[self.theme_name]['text'], relief=tk.RAISED,
                          bd=3, padx=15, pady=15)
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)
        
        # Linien zeichnen
        self._draw_board_lines()
    
    def _draw_board_lines(self) -> None:
        """Zeichnet die Linien des Spielbretts"""
        self.canvas.delete("all")  # Alle vorherigen Linien löschen
        
        # Vertikale Linien
        self.canvas.create_line(110, 10, 110, 310, width=4, fill=THEMES[self.theme_name]['line'])
        self.canvas.create_line(210, 10, 210, 310, width=4, fill=THEMES[self.theme_name]['line'])
        
        # Horizontale Linien
        self.canvas.create_line(10, 110, 310, 110, width=4, fill=THEMES[self.theme_name]['line'])
        self.canvas.create_line(10, 210, 310, 210, width=4, fill=THEMES[self.theme_name]['line'])
    
    def update_display(self, board: List[str], winning_line: Optional[List[int]] = None) -> None:
        """Aktualisiert die Anzeige des Spielbretts"""
        for i in range(9):
            self.buttons[i].config(text=board[i+1])
            
            # Gewinnlinie hervorheben falls vorhanden
            if winning_line and (i+1) in winning_line:
                self.buttons[i].config(bg=THEMES[self.theme_name]['win_highlight'])
            else:
                self.buttons[i].config(bg=THEMES[self.theme_name]['button_bg'])
    
    def update_theme(self, theme_name: str) -> None:
        """Aktualisiert das Farbthema des Spielbretts"""
        self.theme_name = theme_name
        theme = THEMES[self.theme_name]
        
        # Canvas Hintergrund aktualisieren
        self.canvas.configure(bg=theme['bg'])
        
        # Linien neu zeichnen
        self._draw_board_lines()
        
        # Buttons aktualisieren
        for btn in self.buttons:
            btn.configure(
                bg=theme['button_bg'],
                activebackground=theme['button_active_bg'],
                fg=theme['text']
            )
    
    def set_buttons_state(self, state: str) -> None:
        """Setzt den Zustand aller Buttons (normal/disabled)"""
        for btn in self.buttons:
            btn.config(state=state)
