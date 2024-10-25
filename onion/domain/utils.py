from onion.domain.g_settings_bt import settings_ml
from itertools import count

def g_print_load(
    divider=1000, 
    full_load=settings_ml["klines_all"],
):
    # протестить это
    counter = count(start=1)

    def dcrtr(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            current_count = next(counter)
            if current_count % divider == 0:
                print(f"load {func.__name__} - {round(current_count / full_load * 100, 2)}%")
            return res
        return wrapper
    return dcrtr