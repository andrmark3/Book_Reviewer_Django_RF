python -m venv venv

source venv/Scripts/activate

pip install -r src/requirements.txt

python src/manage.py makemigrations

python src/manage.py migrate

echo "|==================================================|"
echo "|          Populate database with data...          |"
echo "|==================================================|"
for py_file in $(find src/fixtures -name "*.json")
do
    python src/manage.py loaddata $py_file
done
echo "|==================================================|"
echo "|         All Fixtures loaded successfully.        |"
echo "|==================================================|"

echo "|==================================================|"
echo "|   Your app is running at http://localhost:8000   |"
echo "|==================================================|"

python src/manage.py runserver 0.0.0.0:8000

