"""
Вспомогательные функции для игры
"""


def display_word(word: str, guessed_letters: set) -> str:
    """Отобразить слово с угаданными буквами"""
    result = []
    for char in word:
        if char in guessed_letters or not char.isalpha():
            result.append(char)
        else:
            result.append('■')
    return ' '.join(result)


def choose_difficulty() -> str:
    """Выбор уровня сложности"""
    while True:
        print("\nВыберите уровень сложности:")
        print("1. Легкий (7 жизней)")
        print("2. Средний (5 жизней)")
        print("3. Сложный (3 жизни)")

        choice = input("Ваш выбор: ").strip()

        if choice in ['1', '2', '3']:
            return choice
        else:
            print("⚠️ Пожалуйста, выберите 1, 2 или 3")


def get_player_input() -> str:
    """Получить ввод от игрока"""
    while True:
        try:
            user_input = input("\nНазовите букву или слово целиком: ").strip()
            if not user_input:
                print("⚠️ Ввод не может быть пустым!")
                continue
            return user_input
        except KeyboardInterrupt:
            print("\nИгра прервана")
            raise
        except Exception as e:
            print(f"⚠️ Ошибка ввода: {e}")
            continue


def format_time(seconds: float) -> str:
    """Форматировать время в читаемый вид"""
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes} мин {seconds} сек"