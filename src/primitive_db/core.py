from primitive_db.utils import load_table_data


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


def insert(metadata, table_name, values):
    """Добавляет новую запись в таблицу,
    проверяя количество и типы значений"""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует')
        return
    table = [i for i in metadata[table_name] if i[0] != "ID"]
    if len(values) != len(table):
        print("Ошибка: неверное количество значений")
        return
    types = {"int": int, "str": str, "bool": bool}
    for i, v in zip(table, values):
        iname, itype = i
        re_type = types[itype]
        if type(v) is not re_type:
            print(f"Ошибка: столбец {iname} ожидает тип {itype}")
            return
    data = load_table_data(table_name)
    max_id = max([i["ID"] for i in data], default=0)
    new_id = max_id + 1
    write = {"ID": new_id}
    for i, v in zip(table, values):
        iname, itype = i
        write[iname] = v
    data.append(write)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return data


def select(table_data, where_clause=None):
    """Возвращает записи с заданным значением where_clause"""
    if where_clause is None:
        return table_data
    for k, v in where_clause.items():
        find = [i for i in table_data if i.get(k) == v]
    return find


def update(table_data, set_clause, where_clause):
    """Изменяет значение по заданному условию"""
    for i in table_data:
        if where_clause.items() <= i.items():
            for k, v in set_clause.items():
                i[k] = v
    return table_data


def delete(table_data, where_clause):
    """Удаляет строку по заданному значению"""
    table_data = [i for i in table_data if not where_clause.items() <= i.items()]
    return table_data
