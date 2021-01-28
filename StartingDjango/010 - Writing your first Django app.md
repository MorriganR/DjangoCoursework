Все досить детально розписано тут:<br>
https://docs.djangoproject.com/en/3.1/intro/tutorial01/

В домашній папці користувача створюємо робочу папку для нашого проєкту, наприклад `sem_work`.
В ній буде код нашого проєкту, а також Virtual Environment для нього.
````
dasha@test_web:~$ pwd
/home/dasha
dasha@test_web:~$ mkdir ./sem_work
dasha@test_web:~$ cd sem_work/
dasha@test_web:~/sem_work$ ll
total 8
drwxrwxr-x 2 dasha dasha 4096 Jan 26 22:22 ./
drwxr-xr-x 8 dasha dasha 4096 Jan 26 22:22 ../
dasha@test_web:~/sem_work$
dasha@test_web:~/sem_work$ python3 -m venv ./venv
dasha@test_web:~/sem_work$ ll
total 12
drwxrwxr-x 3 dasha dasha 4096 Jan 27 00:15 ./
drwxr-xr-x 8 dasha dasha 4096 Jan 26 22:22 ../
drwxrwxr-x 6 dasha dasha 4096 Jan 27 00:15 venv/
dasha@test_web:~/sem_work$ source venv/bin/activate
(venv) dasha@test_web:~/sem_work$
````
Останньою командою активуємо свіжестворені Virtual Environment.

Встановлюємо Django:
````
(venv) dasha@test_web:~/sem_work$
(venv) dasha@test_web:~/sem_work$ python -m django -v
/home/dasha/sem_work/venv/bin/python: No module named django
(venv) dasha@test_web:~/sem_work$ python -m pip install Django
````
...буде багатенсько рядків на екрані...

Можемо глянути що було встановлено:
````
(venv) dasha@test_web:~/sem_work$ python -m pip freeze
asgiref==3.3.1
Django==3.1.5
pkg-resources==0.0.0
pytz==2020.5
sqlparse==0.4.1
(venv) dasha@test_web:~/sem_work$
(venv) dasha@test_web:~/sem_work$ pwd
/home/dasha/sem_work
(venv) dasha@test_web:~/sem_work$ ll
total 12
drwxrwxr-x 3 dasha dasha 4096 Jan 27 00:15 ./
drwxr-xr-x 8 dasha dasha 4096 Jan 26 22:22 ../
drwxrwxr-x 6 dasha dasha 4096 Jan 27 00:15 venv/
(venv) dasha@test_web:~/sem_work$
````

Створюємо наш проєкт,наприклад `semwork`, параметер `./` досить важливий, інакше буде створено папку `semwork`, а вже в ній папку `semwork` з нашим проєктом.<br>
https://docs.djangoproject.com/en/3.1/ref/django-admin/
````
(venv) dasha@test_web:~/sem_work$
(venv) dasha@test_web:~/sem_work$ django-admin startproject semwork ./
(venv) dasha@test_web:~/sem_work$ ll
total 20
drwxrwxr-x 4 dasha dasha 4096 Jan 27 14:24 ./
drwxr-xr-x 8 dasha dasha 4096 Jan 27 08:20 ../
-rwxrwxr-x 1 dasha dasha  663 Jan 27 14:24 manage.py*
drwxrwxr-x 2 dasha dasha 4096 Jan 27 14:24 semwork/
drwxrwxr-x 6 dasha dasha 4096 Jan 27 00:15 venv/
(venv) dasha@test_web:~/sem_work$
````

Далі в файлі `semwork/settings.py`потрібно замінити рядок: `ALLOWED_HOSTS = []` на такий: `ALLOWED_HOSTS = ['*']`

Далі стартуемо тестовий вебсервер Django:
````
(venv) dasha@test_web:~/sem_work$ python manage.py runserver 0:8000
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
January 27, 2021 - 14:28:50
Django version 3.1.5, using settings 'semwork.settings'
Starting development server at http://0:8000/
Quit the server with CONTROL-C.
````

