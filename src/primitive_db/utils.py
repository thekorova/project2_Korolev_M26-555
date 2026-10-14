import json


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
