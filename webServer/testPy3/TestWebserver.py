import sys
sys.path.append(sys.path[0]+"/..")
print(sys.path)

from webServer import WebServer
webserver =WebServer(8080,sys.path[0]+'/webRoot')

while True:
    pass 

