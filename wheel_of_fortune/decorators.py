"""
Модуль с декораторами для игры
"""

import time
import logging
from functools import wraps
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('wheel_of_fortune')


def timer(func):
    """Декоратор для измерения времени выполнения функции"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time

        minutes, seconds = divmod(int(duration), 60)
        time_str = f"{minutes} мин {seconds} сек"

        logger.info(f"Функция {func.__name__} выполнена за {time_str}")
        return result

    return wrapper


def log_errors(func):
    """Декоратор для логирования ошибок"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"{type(e).__name__} - {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise

    return wrapper