import shlex

import prompt

from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """Запускает основной цикл программы"""
    print_help()
    while True:
        metadata = load_metadata("db_meta.json")
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
                metadata = drop_table(metadata, args[1])
                if before_control > len(metadata):
                    save_metadata("db_meta.json", metadata)
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
                    save_metadata("db_meta.json", metadata)
            case _:
                print(f"Функции {args[0]} нет. Попробуйте снова.")
