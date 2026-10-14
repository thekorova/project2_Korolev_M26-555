def create_table(metadata, table_name, columns):
    """Создает таблицу"""
    types = {"int", "str", "bool"}
    columns_names = set()
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует')
        return metadata
    if not columns:
        print("Ошибка: Не указаны столбцы таблицы")
        return metadata
    for i in columns:
        if len(i) != 2:
            print(f"Некорректное значение: {i}. Попробуйте снова.")
            return metadata
        iname, itype = i
        if not iname:
            print("Ошибка: Имя столбца не может быть пустым")
            return metadata
        if itype not in types:
            print(f"Ошибка: {itype} неверный тип данных")
            return metadata
        if iname == "ID" and itype != "int":
            print("Ошибка: Столбец ID должен иметь тип int")
            return metadata
        if iname in columns_names:
            print(f'Ошибка: Столбец "{iname}" уже существует')
            return metadata
        columns_names.add(iname)
    if "ID" in columns_names:
        columns_id = [["ID", "int"]] + [i for i in columns if i[0] != "ID"]
    else:
        columns_id = [["ID", "int"]] + columns
    metadata[table_name] = columns_id
    columns_text = ", ".join(f"{iname}:{itype}" for iname, itype in columns_id)
    print(f'Таблица "{table_name}" успешно создана: со столбцами: {columns_text}')
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу"""
    if table_name in metadata:
        del metadata[table_name]
        print(f'Таблица "{table_name}" успешно удалена')
        return metadata
    else:
        print(f'Ошибка: Таблица "{table_name}" не существует')
        return metadata


def list_tables(metadata):
    """Выводит имена всех таблиц"""
    if not metadata:
        print("Таблиц не существует")
    for i in metadata:
        print(f"- {i}")
