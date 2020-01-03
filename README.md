# WebServer

Web server for Micropython tested an ESP32 and Python 3.7 with support for the execution of Python code

    -> 1 the call http://esp32.home/wupy?Prints("hello world") returns hello world.Only functions of the Wupy class can be called.
    -> 2 in the called html document the mark <wupy eval = 'xxx' /> is replaced by the return value. xxx is any python expression.
