#!/bin/bash

echo "[+] -Installing dependencies - [+]"
sudo pip install -r requeriments.txt

echo "[+] -Creating database"
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata default.json

echo "[+] - Alldone - [+]"
echo "Default username and password"
echo "heimdall:heimdall"
echo "CHANGE THE DEFAUL CREDENTIALS"
