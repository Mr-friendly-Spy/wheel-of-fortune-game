"""
Пакет для игры 'Поле чудес'
"""

from .game import Game
from .file_handler import (
    random_word_generator,
    load_record,
    save_record,
    load_words_count
)
from .decorators import timer, log_errors
from .utils import (
    display_word,
    choose_difficulty,
    get_player_input,
    format_time
)

__version__ = "1.0.0"
__author__ = "Студент"
__all__ = [
    'Game',
    'random_word_generator',
    'load_record',
    'save_record',
    'load_words_count',
    'timer',
    'log_errors',
    'display_word',
    'choose_difficulty',
    'get_player_input',
    'format_time'
]