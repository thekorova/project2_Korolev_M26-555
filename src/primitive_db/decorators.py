import time
from functools import wraps


def handle_db_errors(func):
    """Декаратор для обработки ошибок"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Принимает функцию и обрабатывает ошибки"""
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    return wrapper


def confirm_action(action_name):
    """Запрашивает подтверждение перед выполнением опасной операции."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                i = (
                    input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
                    .strip()
                    .lower()
                )
                if i in ("y", "yes"):
                    return func(*args, **kwargs)
                elif i in ("n", "no"):
                    print("Операция отменена")
                    return None
                else:
                    print("Ошибка: ожидалось значение [y/n]")

        return wrapper

    return decorator


def log_time(func):
    """Замеряет время выполнения функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.monotonic()
            print(f"Функция {func.__name__} выполнилась за {end - start:.3f} секунд")

    return wrapper


def create_cacher():
    """Запоминает кэш для вычеслений"""
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        cache_new = value_func()
        cache[key] = cache_new
        return cache_new

    def clear_cache():
        cache.clear()

    return cache_result, clear_cache
