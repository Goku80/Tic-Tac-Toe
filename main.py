import tkinter as tk
from tkinter import ttk
from typing import List
import random
import time

from constants import Player, Difficulty, DEFAULT_EMOJIS, THEMES
from game_logic import GameLogic
from ui.game_board import GameBoard
from ui.menu import GameMenu
from ui.stats_display import StatsDisplay
from utils.storage import load_stats, save_stats

class TicTacToeGame:
    """Hauptspielklasse, die die Spiellogik enthält"""
    
    def __init__(self):
        # Spieldaten initialisieren
        self.board = [' '] * 10  # Index 0 wird ignoriert
        self.current_player = None
        self.human_emoji = DEFAULT_EMOJIS[Player.HUMAN]
        self.computer_emoji = DEFAULT_EMOJIS[Player.COMPUTER]
        self.difficulty = Difficulty.MEDIUM
        self.game_over = False
        self.winning_line = []
        
        # Spiellogik initialisieren
        self.game_logic = GameLogic()
        
        # Statistiken laden
        self.stats = load_stats()
        
        # UI initialisieren
        self.root = tk.Tk()
        self.root.title("🎮 Tic Tac Toe Deluxe 🎮")
        self.root.minsize(500, 600)
        self.root.configure(bg=THEMES['Hell']['bg'])
        
        # Aktuelle Theme
        self.current_theme = 'Hell'
        
        # Hauptcontainer mit Padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Callbacks für Menüaktionen vorbereiten
        menu_callbacks = {
            'update_emoji': self._update_emojis,
            'update_emoji_category': self._update_emoji_category,
            'update_theme': self._update_theme,
            'update_difficulty': self._update_difficulty,
            'new_game': self.new_game
        }
        
        # UI-Komponenten initialisieren
        self.menu = GameMenu(main_frame, menu_callbacks)
        self.game_board = GameBoard(main_frame, self.current_theme, self._on_player_move)
        self.stats_display = StatsDisplay(main_frame)
        
        # Statistikanzeige initialisieren
        self.stats_display.update_stats(self.stats)
    
    def _update_emoji_category(self, category: str) -> None:
        """Aktualisiert die Emoji-Auswahl basierend auf der gewählten Kategorie"""
        self.menu.update_emoji_list(category)
        self._update_emojis(self.menu.emoji_var.get())
    
    def _update_emojis(self, emoji: str) -> None:
        """Aktualisiert die Emojis für Spieler und Computer"""
        category = self.menu.emoji_cat_var.get()
        available = AVAILABLE_EMOJIS[category].copy()
        
        self.human_emoji = emoji
        # Computer bekommt ein zufälliges anderes Emoji aus der gleichen Kategorie
        if self.human_emoji in available:
            available.remove(self.human_emoji)
        self.computer_emoji = random.choice(available)
        
        # Spielbrett aktualisieren, falls ein Spiel läuft
        self.game_board.update_display(self.board, self.winning_line if self.game_over else None)
    
    def _update_theme(self, theme_name: str) -> None:
        """Aktualisiert das Farbthema des Spiels"""
        self.current_theme = theme_name
        self.root.configure(bg=THEMES[self.current_theme]['bg'])
        self.game_board.update_theme(self.current_theme)
    
    def _update_difficulty(self, difficulty: str) -> None:
        """Aktualisiert den Schwierigkeitsgrad"""
        if difficulty == 'Leicht':
            self.difficulty = Difficulty.EASY
        elif difficulty == 'Mittel':
            self.difficulty = Difficulty.MEDIUM
        else:
            self.difficulty = Difficulty.HARD
    
    def new_game(self) -> None:
        """Startet ein neues Spiel"""
        self.board = [' '] * 10
        self.game_over = False
        self.winning_line = []
        
        # Zufällig bestimmen, wer beginnt
        self.current_player = random.choice([Player.HUMAN, Player.COMPUTER])
        
        # Buttons aktivieren
        self.game_board.set_buttons_state(tk.NORMAL)
        
        # Display aktualisieren
        self.game_board.update_display(self.board)
        
        if self.current_player == Player.HUMAN:
            self.menu.update_status("Du beginnst! Wähle ein Feld.")
        else:
            self.menu.update_status("Computer beginnt...")
            self.root.after(800, self._computer_move)
    
    def _on_player_move(self, position: int) -> None:
        """Verarbeitet einen Spielerzug"""
        if self.game_over or self.current_player != Player.HUMAN:
            return
            
        if self.board[position] == ' ':
            # Spielerzug
            self.board[position] = self.human_emoji
            self.game_board.update_display(self.board)
            
            # Spiel überprüfen
            is_win, winning_line = self.game_logic.check_win(self.board, self.human_emoji)
            if is_win:
                self.game_over = True
                self.winning_line = winning_line
                self.stats.wins += 1
                self.stats.total_games += 1
                save_stats(self.stats)
                self.stats_display.update_stats(self.stats)
                self.menu.update_status("Glückwunsch! Du hast gewonnen! 🎉")
                self.game_board.update_display(self.board, self.winning_line)
                return
                
            if self.game_logic.is_board_full(self.board):
                self.game_over = True
                self.stats.ties += 1
                self.stats.total_games += 1
                save_stats(self.stats)
                self.stats_display.update_stats(self.stats)
                self.menu.update_status("Das Spiel endet unentschieden! 🤝")
                return
                
            # Computer ist dran
            self.current_player = Player.COMPUTER
            self.menu.update_status("Computer denkt nach...")
            self.root.after(800, self._computer_move)
    
    def _computer_move(self) -> None:
        """Führt den Computerzug aus"""
        if self.game_over:
            return
            
        # Zug basierend auf Schwierigkeit wählen
        position = self.game_logic.get_computer_move(
            self.board, self.computer_emoji, self.human_emoji, self.difficulty)
        
        # Computer-Zug ausführen
        self.board[position] = self.computer_emoji
        self.game_board.update_display(self.board)
        
        # Spiel überprüfen
        is_win, winning_line = self.game_logic.check_win(self.board, self.computer_emoji)
        if is_win:
            self.game_over = True
            self.winning_line = winning_line
            self.stats.losses += 1
            self.stats.total_games += 1
            save_stats(self.stats)
            self.stats_display.update_stats(self.stats)
            self.menu.update_status("Der Computer hat gewonnen! 😢")
            self.game_board.update_display(self.board, self.winning_line)
            return
            
        if self.game_logic.is_board_full(self.board):
            self.game_over = True
            self.stats.ties += 1
            self.stats.total_games += 1
            save_stats(self.stats)
            self.stats_display.update_stats(self.stats)
            self.menu.update_status("Das Spiel endet unentschieden! 🤝")
            return
            
        # Spieler ist dran
        self.current_player = Player.HUMAN
        self.menu.update_status("Du bist dran! Wähle ein Feld.")
    
    def run(self) -> None:
        """Startet die Spielschleife"""
        self.root.mainloop()


if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()
