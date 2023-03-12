def outer_func(msg):
    message = msg

    def inner_func():
        print(message)
    return inner_func


m1 = outer_func("yo")
m2 = outer_func("hello")

m1()
m2()
