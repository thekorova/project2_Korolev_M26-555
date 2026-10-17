def parser(value):
    """Преобразует строковое значение в требуемый тип данных"""
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    elif value in ("true", "True"):
        return True
    elif value in ("false", "False"):
        return False
    elif value.lstrip("-").isdigit():
        return int(value)
    else:
        print(f"Ошибка: неверно задано значение: {value}")
        return None


def parser_dict(value):
    """Преобразует входящие данные в словарь"""
    parts = value.split("=", 1)
    if len(parts) != 2:
        print('Ошибка: условие должно содержать один знак "="')
        return None
    k = parts[0].strip()
    v = parts[1].strip()
    if not k:
        print("Ошибка: не указано имя столбца")
        return None
    result = parser(v)
    if result is None:
        return None
    return {k: result}


def parser_incept(values):
    """Преобразует строковое значения список"""
    values = values.strip()
    if not values.startswith("(") or not values.endswith(")"):
        print("Ошибка: значения должны быть заключены в круглые скобки")
        return None
    values = values[1:-1]
    if not values.strip():
        print("Ошибка: список значений пуст")
        return None
    parts = values.split(",")
    re_values = []
    for i in parts:
        i = parser(i)
        if i is None:
            return None
        re_values.append(i)
    return re_values
