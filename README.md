# wheel-of-fortune-game
# Игра "Поле чудес"

## Описание проекта
Упрощенная версия популярной игры "Поле чудес", реализованная на Python с консольным интерфейсом. Игра предназначена для одного игрока и включает систему уровней сложности, подсчет очков и ведение статистики.

## Установка и запуск

### Способ 1: Запуск как Python-пакета

Установка зависимостей (если есть)
pip install -r requirements.txt

Запуск игры
python -m wheel_of_fortune

### Способ 2: Создание исполняемого файла

Установка PyInstaller
pip install pyinstaller

Создание исполняемого файла
pyinstaller --onefile --console wheel_of_fortune/__main__.py --name WheelOfFortune

Запуск исполняемого файла
./dist/WheelOfFortune.exe
