HOST=esp32.home
USER=user
PASSWORD=pw
 
ftp -inv $HOST <<EOF
user $USER $PASSWORD
cd /lib
mput webServer.py
bye
EOF