#!/bin/sh

# Wait until the local Mysql DB container is ready to accept connections
while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done


# Do the migrations first
python manage.py makemigrations
python manage.py migrate


# (Optional) Run the fixtures to populate db.
echo  "|==================================================|"
echo  "|          Populate database with data...          |"
echo  "|==================================================|"
for py_file in $(find fixtures -name "*.json")
do
    python manage.py loaddata $py_file
done
echo  "|==================================================|"
echo  "|         All Fixtures loaded successfully.        |"
echo  "|==================================================|"


# Run the app
echo "|==================================================|"
echo "|   Your app is running at http://localhost:8000   |"
echo "|==================================================|"
python manage.py runserver 0.0.0.0:8000
