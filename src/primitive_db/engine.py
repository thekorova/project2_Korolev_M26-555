import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.constants import META_FILE, VALID_TYPES
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.decorators import create_cacher
from primitive_db.parser import parser_dict, parser_incept
from primitive_db.utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where "
        "<столбец> = <значение> - прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where "
        "<столбец> = <значение> - удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")


def run():
    """Запускает основной цикл программы"""
    print_help()
    cache_result, clear_cache = create_cacher()
    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string("Введите команду: ")
        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Ошибка: Некорректный формат команды.")
            continue
        if not args:
            print("Функции нет. Попробуйте снова.")
            continue
        match args[0]:
            case "help":
                if len(args) > 1:
                    print(f"Некорректное значение: {args[1]}. Попробуйте снова.")
                    continue
                print_help()
            case "exit":
                if len(args) > 1:
                    print(f"Некорректное значение: {args[1]}. Попробуйте снова.")
                    continue
                break
            case "list_tables":
                if len(args) > 1:
                    print(f"Некорректное значение: {args[1]}. Попробуйте снова.")
                    continue
                list_tables(metadata)
            case "drop_table":
                if len(args) < 2:
                    print(
                        "Некорректное значение: имя таблицы отсутствует. "
                        "Попробуйте снова."
                    )
                    continue
                if len(args) > 2:
                    print(f"Некорректное значение: {args[2]}. Попробуйте снова.")
                    continue
                before_control = len(metadata)
                after_control = drop_table(metadata, args[1])
                if after_control is None:
                    continue
                else:
                    metadata = after_control
                if before_control > len(metadata):
                    save_metadata(META_FILE, metadata)
                    delete_table_data(args[1])
                    clear_cache()
            case "create_table":
                if len(args) < 2:
                    print("Некорректное значение: имя таблицы отсутствует.")
                    continue
                table_name = args[1]
                columns = []
                control = True
                for i in args[2:]:
                    isplit = i.split(":")
                    if len(isplit) != 2:
                        print(f"Некорректное значение: {i}. Попробуйте снова.")
                        control = False
                        break
                    name, column_type = isplit
                    columns.append([name, column_type])
                if not control:
                    continue
                before_control = len(metadata)
                metadata = create_table(metadata, table_name, columns)
                if before_control < len(metadata):
                    save_metadata(META_FILE, metadata)
                    clear_cache()
            case "insert":
                if len(args) < 5 or args[1] != "into" or args[3] != "values":
                    print(
                        "Ошибка формата: insert into <имя_таблицы> "
                        "values (ваши значения)"
                    )
                    continue
                table_name = args[2]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует')
                    continue
                values = user_input.split("values")[1].strip()
                values = parser_incept(values)
                if values is None:
                    continue
                data = insert(metadata, table_name, values)
                if data is not None:
                    save_table_data(table_name, data)
                    clear_cache()
            case "select":
                if len(args) < 3 or args[1] != "from":
                    print(
                        "Ошибка формата: select from <имя_таблицы> "
                        "[where <столбец> = <значение>]"
                    )
                    continue
                table_name = args[2]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует')
                    continue
                if len(args) == 3:
                    where_clause = None
                elif len(args) >= 5 and args[3] == "where":
                    values = user_input.split("where")[1].strip()
                    where_clause = parser_dict(values)
                    if where_clause is None:
                        continue
                else:
                    print(
                        "Ошибка формата: select from <имя_таблицы> "
                        "[where <столбец> = <значение>]"
                    )
                    continue
                key = (
                    table_name,
                    tuple(sorted(where_clause.items()))
                    if where_clause is not None
                    else None,
                )
                table = cache_result(
                    key, lambda: select(load_table_data(table_name), where_clause)
                )
                if table is None:
                    continue
                pt = PrettyTable()
                pt.field_names = [column[0] for column in metadata[table_name]]
                for row in table:
                    pt.add_row([row[column] for column in pt.field_names])
                print(pt)
            case "update":
                if len(args) < 6 or args[2] != "set" or "where" not in args[3:]:
                    print(
                        "Ошибка формата: update <имя_таблицы> set <столбец> "
                        "= <значение> where <столбец> = <значение>"
                    )
                    continue
                table_name = args[1]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует')
                    continue
                values = user_input.split("set")[1]
                values_new = values.split("where")[0].strip()
                values_old = values.split("where")[1].strip()
                values_new_pars = parser_dict(values_new)
                values_old_pars = parser_dict(values_old)
                if values_new_pars is None or values_old_pars is None:
                    continue
                meta_table = {i[0]: i[1] for i in metadata[table_name]}
                key_new = list(values_new_pars.keys())[0]
                key_old = list(values_old_pars.keys())[0]
                if key_new not in meta_table or key_old not in meta_table:
                    print("Ошибка: указан несуществующий столбец")
                    continue
                if key_new == "ID":
                    print("Ошибка: менять ID запрещено")
                    continue
                types = VALID_TYPES
                if type(values_new_pars[key_new]) is not types[meta_table[key_new]]:
                    print(
                        f"Ошибка: столбец {key_new} ожидает тип {meta_table[key_new]}"
                    )
                    continue
                if type(values_old_pars[key_old]) is not types[meta_table[key_old]]:
                    print(
                        f"Ошибка: столбец {key_old} ожидает тип {meta_table[key_old]}"
                    )
                    continue
                data = load_table_data(table_name)
                re_value = [i for i in data if values_old_pars.items() <= i.items()]
                if not re_value:
                    print("Записи по заданному условию не найдены")
                    continue
                table = update(data, values_new_pars, values_old_pars)
                if table is None:
                    continue
                save_table_data(table_name, table)
                clear_cache()
                for i in re_value:
                    print(
                        f'Запись с ID={i["ID"]} в таблице "{table_name}" '
                        "успешно обновлена."
                    )
            case "delete":
                if len(args) < 5 or args[1] != "from" or args[3] != "where":
                    print(
                        "Ошибка формата: delete from <имя_таблицы> "
                        "where <столбец> = <значение>"
                    )
                    continue
                table_name = args[2]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует')
                    continue
                values = user_input.split("where")[1].strip()
                where_clause = parser_dict(values)
                if where_clause is None:
                    continue
                data = load_table_data(table_name)
                deleted = [i for i in data if where_clause.items() <= i.items()]
                table = delete(data, where_clause)
                if table is None:
                    continue
                save_table_data(table_name, table)
                clear_cache()
                for i in deleted:
                    print(
                        f"Запись с ID={i['ID']} успешно удалена из "
                        f'таблицы "{table_name}".'
                    )
                if not deleted:
                    print("Записи по заданному условию не найдены")
            case "info":
                if len(args) != 2:
                    print("Ошибка формата: info <имя_таблицы>")
                    continue
                table_name = args[1]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует')
                    continue
                pt = PrettyTable()
                pt.field_names = ["Столбец", "Тип данных"]
                for i in metadata[table_name]:
                    pt.add_row(i)
                print(pt)
            case _:
                print(f"Функции {args[0]} нет. Попробуйте снова.")
