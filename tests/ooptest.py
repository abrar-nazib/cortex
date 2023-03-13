from typing import Any


class dd_class(object):
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, *args: Any, **kwargs: Any):
        print(f"Call method executed before {self.original_function.__name__}")
        return self.original_function(*args, *kwargs)


def dd_ff(original_function):
    def wrapper_function():
        print("Execution inside wrapper")
        return original_function()
    return wrapper_function


@dd_ff
def display():
    print("Display function ran")


@dd_class
def add(a, b):
    print(f"sum = {a+b}")


# decorated_display = decorator_function(display)
# decorated_display()
# display()
add(10, 20)
