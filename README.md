# WebServer

Web server for Micropython tested an ESP32 and Python 3.7 with support for the execution of Python code

    -> 1 the call http://esp32.home/eval?8/4 returns 2.
    -> 2 the call http://esp32.home/exec?print('hallo') prints hallo in the stdout.
    -> 3 in the called html document the mark <wupy eval = 'xxx' /> is replaced by the return value. xxx is any python expression.
    -> 4 in the called html document the mark <wupy exec = 'xxx' /> is replaced by ''''. xxx is any python expression.
