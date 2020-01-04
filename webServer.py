import os
import socket
import sys
import time

import _thread

log_level = 4


class WebServer:

    """ Web server for Micropython and Python 3.7 with support for the execution of Python code
    -> 1 the call http://esp32.home/eval?8/4 returns 2.
    -> 2 the call http://esp32.home/exec?print('hallo') prints hallo in the stdout.
    -> 3 in the called html document the mark <wupy eval = 'xxx' /> is replaced by the return value. xxx is any python expression.
    -> 4 in the called html document the mark <wupy exec = 'xxx' /> is replaced by ''''. xxx is any python expression.
    """

    _mimeTypes = {
        "arc":   "application/x-freearc",
        "bin":   "application/octet-stream",
        "bmp":   "image/bmp",
        "css":   "text/css",
        "csv":   "text/csv",
        "gif":   "image/gif",
        "htm":   "text/html",
        "html":   "text/html",
        "ico":   "image/x-icon",
        "jpeg":   "image/jpeg",
        "jpg":   "image/jpeg",
        "js":   "application/javascript",
        "json":   "application/json",
        "otf":   "font/otf",
        "pdf":   "application/pdf",
        "png":   "image/png",
        "svg":   "image/svg+xml",
        "ts":   "application/typescript",
        "ttf":   "font/ttf",
        "txt":   "text/plain",
        "woff":   "font/woff",
        "woff2":   "font/woff2",
        "xhtml":   "application/xhtml+xml",
        "xml":   "application/xml",
        "zip":   "application/zip"}

    def __init__(self, port=80, webroot="sd/webroot"):
        self.webroot = webroot
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', port))
        self.s.listen(5)
        log_msg(1, "webserver started on port:", port, " webroot: ", webroot)
        _thread.start_new_thread(self._run, ())

    def _getPathAndArgument(self, r):
        """ Splits the request into path, arg, mime and file name """
        request = str(r)
        log_msg(1, 'Content = %s' % request)
        req = request.partition("GET ")
        req = req[2].partition(" HTTP")
        self._path = self.webroot+req[0].partition("?")[0]
        self._arg = req[0].partition("?")[2]
        self._mime = self._path[self._path.rfind(".")+1:len(self._path)]
        self._filename = self._path[self._path.rfind(
            "/")+1:self._path.rfind(".")]
        if self._filename == "":
            self._filename = "index"
            self._mime = "html"
            self._path = self.webroot+"/index.html"

        log_msg(2, 'Path = %s' % str(self._path))
        log_msg(2, 'Arg = %s' % str(self._arg))
        log_msg(2, 'Mime = %s' % str(self._mime))
        log_msg(2, 'Filename = %s' % str(self._filename))

    def _getMimeType(self, mime):
        """ returns the MimeType from mime"""
        for ext in self._mimeTypes:
            if mime == ext:
                return self._mimeTypes[ext]
        return "text/html"

    def _sendFile(self, path, conn):
        try:
            file = open(path, "rb")
            a = True
            while a:
                b = file.read(256)
                if len(b) > 0:
                    conn.send(b)
                else:
                    a = False
            file.close()
            conn.close()
        except Exception as e:
            conn.send('fiel not found')
        conn.close()

    def _sendFileWupy(self, path, conn):
        try:
            file = open(path, "r")
            a = True
            while a:
                b = file.readline()
                if '<wupy' in b:
                    c = b[0:b.find('<wupy')].encode()
                    conn.send(c)
                    if 'eval' in b:
                        c = b[b.find('eval')+4:]
                    if 'exec' in b:
                        c = b[b.find('exec')+4:]
                    if '=' in c:
                        c = c[c.find('=')+1:]
                    if c.find(c.strip()[0]) == 0:
                        h = c.strip()[0]
                        c = c[c.find(h)+1:]
                        run = c[:c.find(h)]
                        c = c[c.find("/>")+2:]
                        if 'eval' in b:
                            log_msg(1, "eval String:", run)
                            try:
                                wup = eval(run, globals(), locals())
                                conn.send(str(wup).encode())
                            except Exception as e:
                                log_msg(1, str(e))
                            
                        if 'exec' in b:
                            run = run.replace("\\n", "\n")
                            log_msg(1, "exec String:", run)
                            try:
                                exec(run, globals(), locals())
                            except Exception as e:
                                log_msg(1, str(e))
                        conn.send(c.encode())
                elif len(b) > 0:
                    conn.send(b.encode())
                else:
                    a = False
            file.close()
            conn.close()
        except Exception as e:
            conn.send('fiel not found')
        conn.close()

    def _execRequest(self, arg, conn):
        arg = arg.replace("%20", " ")
        arg = arg.replace("%22", "'")
        g = arg
        try:
            conn.send(str(exec(g,globals(),locals())).encode())
        except Exception as e:
            conn.send("object has no attribute "+arg)
        conn.close()

    def _evalRequest(self, arg, conn):
        arg = arg.replace("%20", " ")
        arg = arg.replace("%22", "'")
        g = arg
        try:
            conn.send(str(eval(g,globals(),locals())).encode())
        except Exception as e:
            conn.send("object has no attribute "+arg)
        conn.close()

    def _run(self):
        while True:
            conn, addr = self.s.accept()
            self._loop(conn, addr)

    def _loop(self, conn, addr):
        log_msg(1, 'Gots a connection from %s' % str(addr))
        req = conn.recv(1024)
        if len(req) > 2:
            self._getPathAndArgument(req)
            try:
                conn.send(b'HTTP/1.1 200 OK\n')
                s = 'Content-Type: '+self._getMimeType(self._mime)+'\n'
                log_msg(1, s)
                conn.send(s.encode())
                conn.send(b'Connection: close\n\n')
                if self._filename.lower() == "exe":
                    self._execRequest(self._arg, conn)
                if self._filename.lower() == "eva":
                    self._evalRequest(self._arg, conn)
                elif self._mime.lower() in {"html", "htm"}:
                    _thread.start_new_thread(
                        self._sendFileWupy, (self._path, conn))
                else:
                    _thread.start_new_thread(
                        self._sendFile, (self._path, conn))
            except Exception as e:
                sys.print_exception(e)
                conn.close()
        else:
            conn.close()


def log_msg(level, *args):
    if log_level >= level:
        print('webServer: ', *args)
