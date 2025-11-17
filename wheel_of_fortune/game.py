"""
Основной модуль игры
"""

import time
from typing import List, Set
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


class Game:
    """Класс для управления игровым процессом"""

    def __init__(self):
        """Инициализация игры"""
        self.used_words: Set[str] = set()
        self.guessed_words_count = 0
        self.start_time = None
        self.record = load_record()
        self.total_words = load_words_count()

    @log_errors
    def setup_game(self) -> tuple:
        """Настройка игры перед началом"""
        print("=== ПОЛЕ ЧУДЕС ===")
        print(f"🏆 Ваш лучший рекорд: {self.record} слов")

        difficulty = choose_difficulty()
        lives = self._get_lives_by_difficulty(difficulty)

        word_generator = random_word_generator()

        return difficulty, lives, word_generator

    def _get_lives_by_difficulty(self, difficulty: str) -> int:
        """Получить количество жизней по уровню сложности"""
        lives_map = {
            '1': 7,  # Легкий
            '2': 5,  # Средний
            '3': 3  # Сложный
        }
        return lives_map.get(difficulty, 5)

    @log_errors
    @timer
    def play_round(self, word: str, lives: int) -> bool:
        """Играть один раунд с заданным словом"""
        guessed_letters = set()
        word = word.upper()
        attempts = lives

        print(f"\nСлово №{self.guessed_words_count + 1} из {self.total_words}")

        while attempts > 0:
            current_display = display_word(word, guessed_letters)
            print(current_display)
            print(f"Количество жизней: {'♥' * attempts}")

            player_input = get_player_input().upper()

            if len(player_input) > 1:  # Попытка угадать всё слово
                if player_input == word:
                    print(f"\n🎉 Поздравляем! Вы угадали слово: {word}")
                    return True
                else:
                    print("❌ Это не правильное слово!")
                    attempts -= 1
                    continue

            letter = player_input
            if not letter.isalpha() or len(letter) != 1:
                print("⚠️ Пожалуйста, введите одну букву!")
                continue

            if letter in guessed_letters:
                print("⚠️ Вы уже называли эту букву!")
                continue

            guessed_letters.add(letter)

            if letter in word:
                print(f"✅ Буква '{letter}' есть в слове!")
                if all(char in guessed_letters or not char.isalpha() for char in word):
                    print(f"\n🎉 Поздравляем! Вы угадали слово: {word}")
                    return True
            else:
                print(f"❌ Буквы '{letter}' нет в слове!")
                attempts -= 1

        # Если жизни закончились
        print(f"\n💔 ИГРА ОКОНЧЕНА! 💔")
        print(f"К сожалению, у вас закончились жизни.")
        print(f"Загаданное слово было: {word}")
        return False

    @log_errors
    def show_statistics(self, game_duration: float):
        """Показать статистику игры"""
        print(f"\n📊 Ваш результат:")
        print(f"Угадано слов: {self.guessed_words_count} из {self.total_words}")
        print(f"Время игры: {format_time(game_duration)}")
        print(f"Ваш лучший рекорд: {self.record} слов")

        # Проверка на новый рекорд
        if self.guessed_words_count > self.record:
            print(f"\n🎊 НОВЫЙ РЕКОРД! 🎊")
            print(f"Вы установили новый личный рекорд!")
            print(f"Предыдущий рекорд: {self.record} слов")
            print(f"Новый рекорд: {self.guessed_words_count} слов")
            save_record(self.guessed_words_count)
            self.record = self.guessed_words_count

    @log_errors
    def ask_to_continue(self) -> bool:
        """Спросить, хочет ли игрок продолжить"""
        while True:
            answer = input("\nХотите продолжить игру? (да/нет): ").lower()
            if answer in ['да', 'д', 'yes', 'y']:
                return True
            elif answer in ['нет', 'н', 'no', 'n']:
                return False
            else:
                print("⚠️ Пожалуйста, введите 'да' или 'нет'")

    @log_errors
    def run(self):
        """Основной цикл игры"""
        try:
            self.start_time = time.time()

            difficulty, lives, word_generator = self.setup_game()

            for word in word_generator:
                if word in self.used_words:
                    continue

                self.used_words.add(word)

                # Играем раунд
                round_won = self.play_round(word, lives)

                if round_won:
                    self.guessed_words_count += 1

                # Проверяем, все ли слова угаданы
                if len(self.used_words) >= self.total_words:
                    print(f"\n🎉 ПОЗДРАВЛЯЕМ! 🎉")
                    print(f"Вы прошли всю игру и угадали все {self.total_words} слов!")
                    print(f"Вы настоящий ПОБЕДИТЕЛЬ игры 'Поле чудес'!")
                    print(f"\n🏆 ИДЕАЛЬНАЯ ИГРА! 🏆")
                    break

                # Предлагаем продолжить
                if not self.ask_to_continue():
                    break

            # Выводим финальную статистику
            game_duration = time.time() - self.start_time
            self.show_statistics(game_duration)

            print("\n=== ИГРА ЗАВЕРШЕНА ===")
            print("Спасибо за игру!")
            print("До новых встреч в игре 'Поле чудес'!")

        except KeyboardInterrupt:
            print("\n\nИгра прервана пользователем.")
        except Exception as e:
            print(f"\nПроизошла непредвиденная ошибка: {e}")