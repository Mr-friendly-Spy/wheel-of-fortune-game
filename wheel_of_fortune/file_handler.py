"""
Модуль для работы с файлами
"""

import linecache
import random
import os
import sys
from typing import Generator


def get_base_dir():
    """Получить базовую директорию для файлов данных"""
    if getattr(sys, 'frozen', False):
        # Если запущено как исполняемый файл
        base_dir = os.path.dirname(sys.executable)
    else:
        # Если запущено как скрипт
        base_dir = os.path.dirname(os.path.dirname(__file__))
    return base_dir


def get_package_data_dir():
    """Получить путь к папке data внутри пакета"""
    if getattr(sys, 'frozen', False):
        # В режиме исполняемого файла ищем в временной распакованной папке _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            # Это основная папка с распакованными ресурсами
            base_dir = sys._MEIPASS
        else:
            # Резервный вариант - рядом с exe
            base_dir = os.path.dirname(sys.executable)
        data_dir = os.path.join(base_dir, 'data')
    else:
        # В режиме разработки используем относительный путь внутри пакета
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
    return data_dir


def get_words_file_path():
    """Получить путь к файлу со словами"""
    data_dir = get_package_data_dir()
    words_file = os.path.join(data_dir, 'words.txt')
    return words_file


def get_record_file_path():
    """Получить путь к файлу с рекордом"""
    if getattr(sys, 'frozen', False):
        # Сохраняем в папке пользователя (более правильный подход)
        if os.name == 'nt':  # Windows
            base_dir = os.path.join(os.environ['APPDATA'], 'WheelOfFortune')
        else:  # Linux/Mac
            base_dir = os.path.join(os.path.expanduser('~'), '.wheel_of_fortune')
    else:
        # В разработке
        base_dir = os.path.join(os.path.dirname(__file__), 'data')

    return os.path.join(base_dir, 'record.txt')


def random_word_generator() -> Generator[str, None, None]:
    """
    Генератор для чтения случайных слов из файла без повторений
    """
    words_file = get_words_file_path()

    try:
        # Проверяем существование файла
        if not os.path.exists(words_file):
            raise FileNotFoundError(
                f"Файл {words_file} не найден. Убедитесь, что файл words.txt находится в папке data пакета.")

        # Получаем все слова из файла
        with open(words_file, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]

        if not words:
            raise ValueError(f"Файл {words_file} пуст. Добавьте слова в файл.")

        # Перемешиваем слова
        random.shuffle(words)

        for word in words:
            if word:
                yield word

    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("📁 Структура пакета должна быть:")
        print("wheel_of_fortune/")
        print("├── data/")
        print("│   └── words.txt  ← этот файл должен существовать")
        print("└── file_handler.py")
        raise
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла со словами: {e}")


def load_words_count() -> int:
    """Загрузить общее количество слов"""
    words_file = get_words_file_path()

    try:
        if not os.path.exists(words_file):
            raise FileNotFoundError(f"Файл {words_file} не найден")

        with open(words_file, 'r', encoding='utf-8') as f:
            return sum(1 for line in f if line.strip())
    except FileNotFoundError:
        print(f"❌ Файл {words_file} не найден.")
        print("💡 Создайте файл words.txt в папке data со словами для игры.")
        return 0
    except Exception as e:
        print(f"❌ Ошибка при загрузке слов: {e}")
        return 0


def load_record() -> int:
    """Загрузить рекорд из файла"""
    record_file = get_record_file_path()

    try:
        # Создаем папку data, если она не существует (для режима exe)
        data_dir = os.path.dirname(record_file)
        os.makedirs(data_dir, exist_ok=True)

        if os.path.exists(record_file):
            with open(record_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return int(content) if content.isdigit() else 0
        return 0
    except Exception as e:
        print(f"⚠️ Ошибка при загрузке рекорда: {e}")
        return 0


def save_record(record: int):
    """Сохранить рекорд в файл"""
    record_file = get_record_file_path()

    try:
        # Создаем папку data, если она не существует
        data_dir = os.path.dirname(record_file)
        os.makedirs(data_dir, exist_ok=True)

        with open(record_file, 'w', encoding='utf-8') as f:
            f.write(str(record))
        print(f"✅ Рекорд сохранен: {record} слов")
    except Exception as e:
        print(f"❌ Ошибка при сохранении рекорда: {e}")