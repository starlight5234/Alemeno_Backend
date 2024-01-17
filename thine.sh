#!/bin/bash

# Sane sleep time to let the DB service start
sleep 15
echo "Setting up migrations"
python manage.py makemigrations
python manage.py migrate

echo "Importing Data"
python customer_data.py
python loan_data.py

echo "Starting Server"
python manage.py runserver 0.0.0.0:8000
echo "Thine.sh executed"
