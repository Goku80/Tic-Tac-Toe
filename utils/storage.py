import json
import os
from dataclasses import dataclass
from typing import Dict

@dataclass
class GameStats:
    """Spielstatistiken zur Nachverfolgung"""
    wins: int = 0
    losses: int = 0
    ties: int = 0
    total_games: int = 0
    
    def to_dict(self) -> Dict:
        return {
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'total_games': self.total_games
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GameStats':
        return cls(
            wins=data.get('wins', 0),
            losses=data.get('losses', 0),
            ties=data.get('ties', 0),
            total_games=data.get('total_games', 0)
        )

def load_stats() -> GameStats:
    """Lädt Spielstatistiken aus einer Datei oder erstellt neue"""
    try:
        if os.path.exists('tic_tac_toe_stats.json'):
            with open('tic_tac_toe_stats.json', 'r') as f:
                return GameStats.from_dict(json.load(f))
    except Exception as e:
        print(f"Fehler beim Laden der Statistiken: {e}")
    return GameStats()

def save_stats(stats: GameStats) -> None:
    """Speichert die aktuellen Spielstatistiken"""
    try:
        with open('tic_tac_toe_stats.json', 'w') as f:
            json.dump(stats.to_dict(), f)
    except Exception as e:
        print(f"Fehler beim Speichern der Statistiken: {e}")