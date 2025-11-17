"""
Точка входа в игру 'Поле чудес'
"""

from wheel_of_fortune.game import Game

def main():
    """Основная функция запуска игры"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()