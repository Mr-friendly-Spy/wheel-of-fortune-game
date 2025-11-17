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
        return os.path.dirname(sys.executable)
    else:
        # Если запущено как скрипт
        return os.path.dirname(os.path.dirname(__file__))


def get_data_dir():
    """Получить путь к папке с данными"""
    base_dir = get_base_dir()
    data_dir = os.path.join(base_dir, 'data')

    # Создаем папку, если её нет
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)

    return data_dir


def get_words_file_path():
    """Получить путь к файлу со словами"""
    data_dir = get_data_dir()
    words_file = os.path.join(data_dir, 'words.txt')

    # Если файл не найден, создаем его с примерами
    if not os.path.exists(words_file):
        create_default_words_file(words_file)

    return words_file


def get_record_file_path():
    """Получить путь к файлу с рекордом"""
    data_dir = get_data_dir()
    return os.path.join(data_dir, 'record.txt')


def create_default_words_file(words_file: str):
    """Создать файл со словами по умолчанию"""
    default_words = [
        "программирование", "компьютер", "алгоритм", "интерфейс", "разработка",
        "технология", "искусственный", "нейросеть", "машинное", "обучение",
        "питон", "декоратор", "генератор", "исключение", "модуль",
        "программа", "функция", "переменная", "список", "словарь"
    ]

    try:
        with open(words_file, 'w', encoding='utf-8') as f:
            for word in default_words:
                f.write(word + '\n')
        print(f"✅ Создан файл со словами: {words_file}")
    except Exception as e:
        print(f"❌ Ошибка при создании файла слов: {e}")


def random_word_generator() -> Generator[str, None, None]:
    """
    Генератор для чтения случайных слов из файла без повторений
    """
    words_file = get_words_file_path()

    try:
        # Получаем все слова из файла
        with open(words_file, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]

        if not words:
            raise ValueError("Файл со словами пуст")

        # Перемешиваем слова
        random.shuffle(words)

        for word in words:
            if word:
                yield word

    except Exception as e:
        raise Exception(f"Ошибка при чтении файла со словами: {e}")


def load_words_count() -> int:
    """Загрузить общее количество слов"""
    words_file = get_words_file_path()

    try:
        with open(words_file, 'r', encoding='utf-8') as f:
            return sum(1 for line in f if line.strip())
    except Exception as e:
        print(f"❌ Ошибка при загрузке слов: {e}")
        return 20  # Возвращаем значение по умолчанию


def load_record() -> int:
    """Загрузить рекорд из файла"""
    record_file = get_record_file_path()

    try:
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
        with open(record_file, 'w', encoding='utf-8') as f:
            f.write(str(record))
    except Exception as e:
        print(f"❌ Ошибка при сохранении рекорда: {e}")