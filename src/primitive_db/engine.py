import prompt


def welcome():
    """Обрабатывает команды программы"""
    print("Первая попытка запустить проект!\n\n***")
    while True:
        print("<command> exit - выйти из программы")
        print("<command> help - справочная информация")
        command = prompt.string("Введите команду: ")

        if command == "exit":
            print("Завершение программы.")
            break
        if command == "help":
            print()
            continue
        else:
            print(f"\nНеизвестная команда: {command}\n")
