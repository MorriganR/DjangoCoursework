## Usage

- Clone repository and enter project directory
```
git clone https://github.com/MorriganR/DjangoCoursework.git
cd DjangoCoursework
```

- Create virtual enviroment 
```
python -m venv venvdev
```

- Activate virtual enviroment
```
.\venvdev\Scripts\activate.bat
```

- Install all dependencies 
```
pip install -r requirements.txt
```

- Init & restore sqlite database
```
python manage.py migrate
python manage.py loaddata --format json db.json
```

- Run server 
```
python manage.py runserver
```

Django admin credentials: admin admin1234

For sync local/main with remote/origin/main:
```
git fetch origin
git checkout -B main origin/main
```

Create new migrations if models in models.py is changed:
```
python manage.py makemigrations gausscourse
python manage.py migrate
```

How to dump/restore the DB:
```
python manage.py dumpdata --natural-foreign --natural-primary --indent 2 --format json > db.json
# Removes all data from the database: python manage.py flush
python manage.py loaddata --format json db.json
```