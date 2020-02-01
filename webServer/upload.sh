HOST=esp32.home
USER=user
PASSWORD=pw
DIRECTORY="/lib"
WEBROOT="/sd/webroot"


echo "mkdir"
echo "***************"

ftp -inv $HOST <<EOF
user $USER $PASSWORD
mkdir $DIRECTORY
bye
EOF
 
ftp -inv $HOST <<EOF
user $USER $PASSWORD
cd /lib
mput webServer.py
bye
EOF

cd testPy3
cd webRoot


ftp -inv $HOST <<EOF
user $USER $PASSWORD
cd /sd
cd /webroot
mput favicon.ico
mput index.html
bye
EOF
cd ..
cd ..



