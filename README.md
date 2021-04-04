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

- Init sqlite database
```
python manage.py migrate
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