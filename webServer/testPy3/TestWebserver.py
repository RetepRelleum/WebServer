import sys
sys.path.append(sys.path[0]+"/..")
print(sys.path)

from webServer import WebServer
webserver =WebServer(sys.path[0]+'/webRoot',8080)

while True:
    pass 

