from enum import Enum, auto
from typing import Dict, List

# Player und Difficulty Enums
class Player(Enum):
    HUMAN = auto()
    COMPUTER = auto()

class Difficulty(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()

# Emoji-Auswahl mit Defaultwerten
DEFAULT_EMOJIS = {
    Player.HUMAN: '🦁',
    Player.COMPUTER: '🦊'
}

# Erweiterte Emoji-Sammlung
AVAILABLE_EMOJIS = {
    'Tiere': ['🦁', '🦊', '🐶', '🐱', '🐼', '🐨', '🐸', '🦄', '🦖', '🐙'],
    'Obst': ['🍎', '🍌', '🍓', '🍉', '🍇', '🍒', '🥝', '🍍', '🥥', '🍑'],
    'Gesichter': ['😊', '😎', '🤩', '😍', '🥰', '🤔', '🙄', '😜', '🥳', '😇'],
    'Symbole': ['❤️', '⭐', '✨', '🔥', '💯', '🌈', '☀️', '🌙', '⚡', '💫']
}

# Farbthemen für das Spielfeld
THEMES = {
    'Hell': {
        'bg': '#F5F5F5',
        'button_bg': '#FFFFFF',
        'button_active_bg': '#E0E0E0',
        'text': '#333333',
        'line': '#555555',
        'title': '#222222',
        'win_highlight': '#4CAF50'
    },
    'Dunkel': {
        'bg': '#2D2D2D',
        'button_bg': '#3D3D3D',
        'button_active_bg': '#4D4D4D',
        'text': '#E0E0E0',
        'line': '#BBBBBB',
        'title': '#FFFFFF',
        'win_highlight': '#8BC34A'
    },
    'Blau': {
        'bg': '#E3F2FD',
        'button_bg': '#BBDEFB',
        'button_active_bg': '#90CAF9',
        'text': '#1565C0',
        'line': '#1976D2',
        'title': '#0D47A1',
        'win_highlight': '#4FC3F7'
    },
    'Rosa': {
        'bg': '#FCE4EC',
        'button_bg': '#F8BBD0',
        'button_active_bg': '#F48FB1',
        'text': '#C2185B',
        'line': '#D81B60',
        'title': '#880E4F',
        'win_highlight': '#F06292'
    }
}