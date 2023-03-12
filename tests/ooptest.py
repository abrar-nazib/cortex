def logger(msg: str):
    def log_message():
        print('Log: ', msg)
    return log_message


message_logger1 = logger("mairala")
message_logger2 = logger("kaittala")

message_logger1()
message_logger2()
