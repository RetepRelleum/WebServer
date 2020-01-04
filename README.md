# WebServer

Web server for Micropython tested an ESP32 and Python 3.7 with support for the execution of Python code

1 the call http://esp32.home/eval?8/4 returns 2.

2 the call http://esp32.home/exec?print('hallo') prints hallo in the stdout.

3 in the called html document the mark <wupy eval = 'xxx' /> is replaced by the return value. xxx is any python expression.

4 in the called html document the mark <wupy exec = 'xxx' /> is replaced by ''''. xxx is any python expression.

## Example:

    <h1>time related functions</h1>
    <table>
        <tr>
            <th>Convert a time expressed in seconds since the Epoch</th>
            <th>
                <wupy eval="time.localtime()" />
            </th>
        </tr>
        <tr>
            <th>The number of seconds, as an integer, since the Epoch</th>
            <th>
                <wupy eval="time.time()" />
            </th>
        </tr>
    </table>

    <script>
        $(document).ready(function () {
            $("button").click(function () {
                $.get("exec?machine.Pin(5,machine.Pin.OUT).value(0)", function (data, status) {
                    alert("Data: " + data + "\nStatus: " + status);
                });
            });
        });
    </script>

    <button>led on at ESP32 lolin pro</button>