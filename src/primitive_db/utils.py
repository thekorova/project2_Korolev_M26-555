import json
import os


def load_metadata(filepath):
    """Загружает данные из json"""
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет данные в json"""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def load_table_data(table_name):
    """Загружает данные json в директории data,
    если файла нет, возвращает пустой список."""
    filepath = os.path.join("data", f"{table_name}.json")
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет данные json в директории data,
    создает папку data, если ее нет."""
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def delete_table_data(table_name):
    """Удаляет json с данными таблицы."""
    filepath = os.path.join("data", f"{table_name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
