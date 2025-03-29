import random
from typing import List, Optional, Tuple
from constants import Difficulty, Player

class GameLogic:
    def check_win(self, board: List[str], emoji: str) -> Tuple[bool, List[int]]:
        """Überprüft, ob ein Spieler gewonnen hat und gibt Gewinnlinie zurück"""
        win_combinations = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],  # horizontale Linien
            [1, 4, 7], [2, 5, 8], [3, 6, 9],  # vertikale Linien
            [1, 5, 9], [3, 5, 7]              # diagonale Linien
        ]
        
        for line in win_combinations:
            if all(board[pos] == emoji for pos in line):
                return True, line
                
        return False, []
    
    def is_board_full(self, board: List[str]) -> bool:
        """Überprüft, ob das Spielbrett voll ist"""
        return ' ' not in board[1:]
    
    def get_computer_move(self, board: List[str], computer_emoji: str, 
                         human_emoji: str, difficulty: Difficulty) -> int:
        """Berechnet den besten Zug für den Computer basierend auf dem Schwierigkeitsgrad"""
        # Bei leichtem Schwierigkeitsgrad: Manchmal zufälliger Zug
        if difficulty == Difficulty.EASY and random.random() < 0.5:
            empty_spots = [i for i in range(1, 10) if board[i] == ' ']
            return random.choice(empty_spots) if empty_spots else -1
        
        # Gewinnzug suchen
        for i in range(1, 10):
            if board[i] == ' ':
                board_copy = board.copy()
                board_copy[i] = computer_emoji
                if self.check_win(board_copy, computer_emoji)[0]:
                    return i
        
        # Blockiere den Spieler, wenn er gewinnen könnte
        for i in range(1, 10):
            if board[i] == ' ':
                board_copy = board.copy()
                board_copy[i] = human_emoji
                if self.check_win(board_copy, human_emoji)[0]:
                    return i
        
        # Bei mittlerem Schwierigkeitsgrad: Manchmal strategisch suboptimaler Zug
        if difficulty == Difficulty.MEDIUM and random.random() < 0.3:
            empty_spots = [i for i in range(1, 10) if board[i] == ' ']
            return random.choice(empty_spots) if empty_spots else -1
        
        # Strategische Züge
        # Zentrum nehmen wenn frei
        if board[5] == ' ':
            return 5
            
        # Ecken nehmen wenn frei
        corners = [1, 3, 7, 9]
        empty_corners = [c for c in corners if board[c] == ' ']
        if empty_corners:
            return random.choice(empty_corners)
            
        # Seiten nehmen wenn frei
        sides = [2, 4, 6, 8]
        empty_sides = [s for s in sides if board[s] == ' ']
        if empty_sides:
            return random.choice(empty_sides)
            
        # Sollte nie erreicht werden, wenn noch Felder frei sind
        return -1
