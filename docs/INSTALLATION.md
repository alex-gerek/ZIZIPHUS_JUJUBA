# ZIZIPHUS JUJUBA: Руководство по установке и запуску (Installation & Quickstart)

## 1. Системные требования
* **Операционная система:** Windows 10 / 11 (64-bit), Linux (Ubuntu 20.04+), macOS (12+).
* **Python:** 3.10 – 3.14 (AMD64).
* **Свободное место на диске:** от 500 МБ.
* **Браузер:** Любой современный браузер (Chrome, Edge, Firefox) с поддержкой WebGL и JavaScript.

---

## 2. Установка зависимостей

1. Клонируйте репозиторий в локальную директорию:
   ```bash
   git clone <URL_РЕПОЗИТОРИЯ> D:\Projects\ZIZIPHUS_JUJUBA
   cd D:\Projects\ZIZIPHUS_JUJUBA
   ```

2. (Рекомендуется) Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # На Windows
   # source .venv/bin/activate  # На Linux/macOS
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Запуск лаборатории

### Вариант A (Один клик на Windows):
Запустите файл `start.bat` или кликните ярлык **ZIZIPHUS JUJUBA** на Рабочем столе.
Лаунчер автоматически:
* Проверит наличие и целостность базы данных SQLite `data/database/ziziphus_jujuba.db`.
* При необходимости пересоберет нормализованные таблицы из первичных логов.
* Запустит локальный веб-сервер Uvicorn на `http://127.0.0.1:8765`.
* Автоматически откроет интерфейс исследовательской лаборатории в браузере по умолчанию.

### Вариант B (Командная строка):
```bash
python run_app.py
```
Или напрямую через uvicorn:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8765 --reload
```

---

## 4. Запуск автоматических тестов
Для проверки математических моделей, парсера логов, аудита и целостности базы данных:
```bash
python -m unittest discover tests
```
Все 17+ тестов должны завершиться со статусом `OK`.
